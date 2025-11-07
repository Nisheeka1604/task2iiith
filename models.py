from sqlalchemy import Column, String, Float
from database import Base

class WaterQuality(Base):
    __tablename__ = "water_quality"

    node_id = Column(String(50), primary_key=True)
    tds = Column(Float)
    turbidity = Column(Float)
    ph = Column(Float)
    temperature = Column(Float)

class AirQuality(Base):
    __tablename__ = "air_quality"

    node_id = Column(String(50), primary_key=True)
    pm2_5 = Column(Float)
    pm10 = Column(Float)
    temperature = Column(Float)
    humidity = Column(Float)
    relative_humidity = Column(Float)
    co2 = Column(Float)
    noise = Column(Float)
