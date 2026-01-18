from fastapi import APIRouter
from app.api.routers.auth import router as auth_router
from app.api.routers.accounts import router as accounts_router
from app.api.routers.transfers import router as transfers_router
from app.api.routers.currencies import router as currencies_router

api_v1_router = APIRouter()
api_v1_router.include_router(auth_router)
api_v1_router.include_router(accounts_router)
api_v1_router.include_router(transfers_router)
api_v1_router.include_router(currencies_router)