from fastapi import FastAPI
from app.api.routers import auth_router, accounts_router, transfers_router

app = FastAPI(title="FastAPI Clean Architecture CRUD + Auth + Transactions")

app.include_router(auth_router)
app.include_router(accounts_router)
app.include_router(transfers_router)


@app.get("/health")
def health():
    return {"status": "ok"}
