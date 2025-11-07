from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

# Water Quality Schemas
class WaterQualityBase(BaseModel):
    node_id: str = Field(..., description="Unique identifier for the node")
    tds: Optional[float] = Field(None, description="Total Dissolved Solids")
    turbidity: Optional[float] = Field(None, description="Water turbidity level")
    ph: Optional[float] = Field(None, description="pH level of water")
    temperature: Optional[float] = Field(None, description="Water temperature in Celsius")

class WaterQualityCreate(WaterQualityBase):
    pass

class WaterQuality(WaterQualityBase):
    class Config:
        from_attributes = True

# Air Quality Schemas
class AirQualityBase(BaseModel):
    node_id: str = Field(..., description="Unique identifier for the node")
    pm2_5: Optional[float] = Field(None, description="PM2.5 particulate matter")
    pm10: Optional[float] = Field(None, description="PM10 particulate matter")
    temperature: Optional[float] = Field(None, description="Air temperature in Celsius")
    humidity: Optional[float] = Field(None, description="Air humidity percentage")
    relative_humidity: Optional[float] = Field(None, description="Relative humidity percentage")
    co2: Optional[float] = Field(None, description="CO2 level in ppm")
    noise: Optional[float] = Field(None, description="Noise level in dB")

class AirQualityCreate(AirQualityBase):
    pass

class AirQuality(AirQualityBase):
    class Config:
        from_attributes = True
