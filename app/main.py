from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.v1.router import api_v1_router
from app.core.config import settings
from app.errors import Conflict, DomainError, Forbidden, InsufficientFunds, NotFound

app = FastAPI(title="Banking API")

origins = settings.cors_origins_list or ["http://localhost:5173"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_v1_router, prefix="/api/v1")

ERROR_STATUS_MAP = {
    NotFound: 404,
    Forbidden: 403,
    Conflict: 409,
    InsufficientFunds: 400,
}


@app.exception_handler(DomainError)
def handle_domain_error(request: Request, exc: DomainError) -> JSONResponse:
    status_code = ERROR_STATUS_MAP.get(type(exc), 400)
    return JSONResponse(status_code=status_code, content={"detail": str(exc)})


@app.get("/health")
def health():
    return {"status": "ok"}
