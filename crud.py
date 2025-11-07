from sqlalchemy.orm import Session
import models
import schemas

# Water Quality CRUD operations
def get_water_quality_data(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.WaterQuality).offset(skip).limit(limit).all()

def get_water_quality_by_node(db: Session, node_id: str):
    return db.query(models.WaterQuality).filter(models.WaterQuality.node_id == node_id).first()

def create_water_quality_data(db: Session, data: schemas.WaterQualityCreate):
    db_data = models.WaterQuality(**data.dict())
    db.add(db_data)
    db.commit()
    db.refresh(db_data)
    return db_data

# Air Quality CRUD operations
def get_air_quality_data(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.AirQuality).offset(skip).limit(limit).all()

def get_air_quality_by_node(db: Session, node_id: str):
    return db.query(models.AirQuality).filter(models.AirQuality.node_id == node_id).first()

def create_air_quality_data(db: Session, data: schemas.AirQualityCreate):
    db_data = models.AirQuality(**data.dict())
    db.add(db_data)
    db.commit()
    db.refresh(db_data)
    return db_data
