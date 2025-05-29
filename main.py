from fastapi import FastAPI
from app.routers import auth_router, test_router
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI(
    title="Inventra API",
    description="Inventory Management System with FastAPI + MongoDB Atlas",
    version="0.1.0"
)

origins = [
    "http://localhost:3000",
    "exp://192.168.0.159:8081",
    "http://localhost:8081",
    "http://192.168.0.159:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router.router, prefix="/api/auth", tags=["Auth"])
app.include_router(test_router.router, prefix="/test", tags=["Role Test"])

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)