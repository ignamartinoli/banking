from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.router import api_v1_router

app = FastAPI(title="FastAPI Clean Architecture CRUD + Auth + Transactions")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # add your Railway frontend domain later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(api_v1_router, prefix="/api/v1")


@app.get("/health")
def health():
    return {"status": "ok"}
