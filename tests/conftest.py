import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.api import deps
from app.db.base import Base
from app.db.models import Currency


API_PREFIX = "/api/v1"


@pytest.fixture(scope="session")
def engine():
    engine = create_engine(
        "sqlite+pysqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)
    return engine


@pytest.fixture(scope="function")
def db_session(engine):
    """
    Transaction-per-test pattern:
    - Start a transaction
    - Use one session bound to that connection
    - Roll back after test -> clean slate
    """
    connection = engine.connect()
    transaction = connection.begin()
    TestingSessionLocal = sessionmaker(bind=connection, autoflush=False, autocommit=False)

    session = TestingSessionLocal()

    try:
        yield session
    finally:
        session.close()
        transaction.rollback()
        connection.close()


def seed_currencies(session):
    # Ensure ARS/EUR/USD exist for every test
    session.add_all([Currency(code="ARS"), Currency(code="EUR"), Currency(code="USD")])
    session.commit()


@pytest.fixture(scope="function")
def client(db_session):
    seed_currencies(db_session)

    def override_get_db():
        try:
            yield db_session
        finally:
            # Don't commit here; tests control data explicitly
            pass

    app.dependency_overrides[deps.get_db] = override_get_db

    with TestClient(app) as c:
        yield c

    app.dependency_overrides.clear()


@pytest.fixture(scope="session", autouse=True)
def dispose_engine(engine):
    yield
    engine.dispose()


def register_and_get_token(client: TestClient, email: str, password: str) -> str:
    r = client.post(f"{API_PREFIX}/auth/register", json={"email": email, "password": password})
    assert r.status_code == 200, r.text
    return r.json()["access_token"]


def auth_headers(token: str) -> dict:
    return {"Authorization": f"Bearer {token}"}