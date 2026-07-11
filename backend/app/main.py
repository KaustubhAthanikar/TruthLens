from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.routes import image_routes
from app.database.mongodb import (connect_database,close_database)
from app.routes.claim_routes import router as claim_router

@asynccontextmanager
async def lifespan(app:FastAPI):
    await connect_database()

    yield

    await close_database()

app = FastAPI(
    title='TruthLens',
    version='1.0',
    lifespan=lifespan
)

origins = [
    "http://localhost:5173",
    "http://localhost:5174",
    "https://truth-lens-kappa-nine.vercel.app"
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(claim_router)
app.include_router(image_routes.router)

@app.get("/")
async def home():
    return {
        "message":"Backend running"
    }