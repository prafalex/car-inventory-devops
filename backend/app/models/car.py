from sqlalchemy import Column, Integer, String, Float
from app.database import Base


class Car(Base):
    __tablename__ = "cars"

    id = Column(Integer, primary_key=True, index=True)
    brand = Column(String, nullable=False)
    model = Column(String, nullable=False)
    year = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)
    fuel = Column(String, nullable=False)  # petrol, diesel, electric, hybrid, hydrogen
    mileage = Column(Integer, nullable=False)
    color = Column(String, nullable=True)


# Future field: engine_type could be added here v02
# Future field: repairs could be added here v02
