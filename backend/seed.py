import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from app.database import SessionLocal, engine, Base
from app.models.car import Car

Base.metadata.create_all(bind=engine)

cars = [
    Car(brand="BMW",        model="3 Series",   year=2022, price=42000, fuel="petrol",   mileage=18000,  color="Black"),
    Car(brand="BMW",        model="X5",          year=2021, price=68000, fuel="diesel",   mileage=32000,  color="White"),
    Car(brand="Audi",       model="A4",          year=2023, price=45000, fuel="petrol",   mileage=8000,   color="Gray"),
    Car(brand="Audi",       model="Q7",          year=2020, price=72000, fuel="diesel",   mileage=55000,  color="Blue"),
    Car(brand="Mercedes",   model="C-Class",     year=2022, price=52000, fuel="petrol",   mileage=21000,  color="Silver"),
    Car(brand="Mercedes",   model="GLE",         year=2021, price=89000, fuel="hybrid",   mileage=28000,  color="Black"),
    Car(brand="Volkswagen", model="Golf",        year=2023, price=28000, fuel="petrol",   mileage=5000,   color="Red"),
    Car(brand="Volkswagen", model="Passat",      year=2020, price=31000, fuel="diesel",   mileage=61000,  color="White"),
    Car(brand="Toyota",     model="Corolla",     year=2022, price=24000, fuel="hybrid",   mileage=14000,  color="Blue"),
    Car(brand="Toyota",     model="RAV4",        year=2023, price=38000, fuel="hybrid",   mileage=7000,   color="Gray"),
    Car(brand="Tesla",      model="Model 3",     year=2023, price=55000, fuel="electric", mileage=12000,  color="White"),
    Car(brand="Tesla",      model="Model Y",     year=2022, price=62000, fuel="electric", mileage=19000,  color="Red"),
    Car(brand="Ford",       model="Focus",       year=2021, price=21000, fuel="petrol",   mileage=38000,  color="Orange"),
    Car(brand="Ford",       model="Mustang",     year=2022, price=58000, fuel="petrol",   mileage=9000,   color="Black"),
    Car(brand="Porsche",    model="Cayenne",     year=2022, price=95000, fuel="hybrid",   mileage=15000,  color="Silver"),
    Car(brand="Porsche",    model="911",         year=2021, price=120000,fuel="petrol",   mileage=22000,  color="Yellow"),
    Car(brand="Renault",    model="Megane",      year=2022, price=22000, fuel="petrol",   mileage=27000,  color="Blue"),
    Car(brand="Skoda",      model="Octavia",     year=2023, price=26000, fuel="diesel",   mileage=6000,   color="Gray"),
    Car(brand="Dacia",      model="Duster",      year=2022, price=18000, fuel="petrol",   mileage=33000,  color="Green"),
    Car(brand="Honda",      model="Civic",       year=2023, price=29000, fuel="hybrid",   mileage=4000,   color="White"),
]

db = SessionLocal()
db.add_all(cars)
db.commit()
db.close()
print("Seeded 20 cars successfully.")
