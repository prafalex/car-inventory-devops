from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import cars
from app.database import engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Car Inventory API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(cars.router, prefix="/api/cars", tags=["cars"])


@app.get("/health")
def health_check():
    return {"status": "ok", "service": "car-inventory-backend"}
