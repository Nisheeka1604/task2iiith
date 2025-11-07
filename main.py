from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from database import get_db, engine
from models import Base
import crud
import schemas

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="IoT Data API", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000", "http://localhost:3001", "http://127.0.0.1:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "IoT Data API is running"}

# Water Quality endpoints
@app.get("/water-quality/", response_model=list[schemas.WaterQuality])
def get_water_quality_data(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all water quality data with pagination"""
    return crud.get_water_quality_data(db, skip=skip, limit=limit)

@app.get("/water-quality/{node_id}", response_model=schemas.WaterQuality)
def get_water_quality_by_node(node_id: str, db: Session = Depends(get_db)):
    """Get water quality data by node ID"""
    data = crud.get_water_quality_by_node(db, node_id=node_id)
    if data is None:
        raise HTTPException(status_code=404, detail="Water quality data not found")
    return data

@app.post("/water-quality/", response_model=schemas.WaterQuality)
def create_water_quality_data(data: schemas.WaterQualityCreate, db: Session = Depends(get_db)):
    """Create new water quality data entry"""
    return crud.create_water_quality_data(db=db, data=data)

# Air Quality endpoints
@app.get("/air-quality/", response_model=list[schemas.AirQuality])
def get_air_quality_data(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all air quality data with pagination"""
    return crud.get_air_quality_data(db, skip=skip, limit=limit)

@app.get("/air-quality/{node_id}", response_model=schemas.AirQuality)
def get_air_quality_by_node(node_id: str, db: Session = Depends(get_db)):
    """Get air quality data by node ID"""
    data = crud.get_air_quality_by_node(db, node_id=node_id)
    if data is None:
        raise HTTPException(status_code=404, detail="Air quality data not found")
    return data

@app.post("/air-quality/", response_model=schemas.AirQuality)
def create_air_quality_data(data: schemas.AirQualityCreate, db: Session = Depends(get_db)):
    """Create new air quality data entry"""
    return crud.create_air_quality_data(db=db, data=data)
