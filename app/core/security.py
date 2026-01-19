from datetime import datetime, timedelta, timezone
import hashlib

import jwt
from jwt import InvalidTokenError, ExpiredSignatureError

from passlib.context import CryptContext
from app.core.config import settings


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def _prehash(password: str) -> str:
    # Normalize + prehash to avoid bcrypt 72-byte limit issues
    # (and avoid weird unicode edge cases)
    normalized = password.strip()
    digest = hashlib.sha256(normalized.encode("utf-8")).hexdigest()
    return digest


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(password: str, password_hash: str) -> bool:
    return pwd_context.verify(password, password_hash)


def create_access_token(subject: str) -> str:
    now = datetime.now(timezone.utc)
    exp = datetime.now(timezone.utc) + timedelta(
        minutes=settings.access_token_expire_minutes
    )

    payload = {
        "sub": subject,
        "iat": now,  # PyJWT accepts datetimes and will convert to numeric dates
        "exp": exp,
    }

    return jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algorithm)


def decode_token(token: str) -> dict:
    # Raises ExpiredSignatureError / InvalidTokenError on failure
    return jwt.decode(
        token,
        settings.jwt_secret,
        algorithms=[settings.jwt_algorithm],
        options={"require": ["exp", "sub"]},
    )

