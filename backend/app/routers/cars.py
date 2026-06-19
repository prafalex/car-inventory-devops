from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel, field_validator
from typing import Optional, List
from app.database import get_db
from app.models.car import Car

router = APIRouter()


class CarCreate(BaseModel):
    brand: str
    model: str
    year: int
    price: float
    fuel: str
    mileage: int
    color: Optional[str] = None

    @field_validator("price")
    @classmethod
    def price_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError("price must be greater than 0")
        return v

    @field_validator("mileage")
    @classmethod
    def mileage_must_be_non_negative(cls, v):
        if v < 0:
            raise ValueError("mileage cannot be negative")
        return v

class CarResponse(CarCreate):
    id: int

    class Config:
        from_attributes = True


@router.get("/", response_model=List[CarResponse])
def list_cars(brand: Optional[str] = None, db: Session = Depends(get_db)):
    query = db.query(Car)
    if brand:
        query = query.filter(Car.brand.ilike(f"%{brand}%"))
    return query.all()


@router.get("/{car_id}", response_model=CarResponse)
def get_car(car_id: int, db: Session = Depends(get_db)):
    car = db.query(Car).filter(Car.id == car_id).first()
    if not car:
        raise HTTPException(status_code=404, detail="Car not found")
    return car


@router.post("/", response_model=CarResponse, status_code=201)
def create_car(car: CarCreate, db: Session = Depends(get_db)):
    db_car = Car(**car.model_dump())
    db.add(db_car)
    db.commit()
    db.refresh(db_car)
    return db_car


@router.put("/{car_id}", response_model=CarResponse)
def update_car(car_id: int, car: CarCreate, db: Session = Depends(get_db)):
    db_car = db.query(Car).filter(Car.id == car_id).first()
    if not db_car:
        raise HTTPException(status_code=404, detail="Car not found")
    for key, value in car.model_dump().items():
        setattr(db_car, key, value)
    db.commit()
    db.refresh(db_car)
    return db_car


@router.delete("/{car_id}", status_code=204)
def delete_car(car_id: int, db: Session = Depends(get_db)):
    db_car = db.query(Car).filter(Car.id == car_id).first()
    if not db_car:
        raise HTTPException(status_code=404, detail="Car not found")
    db.delete(db_car)
    db.commit()
