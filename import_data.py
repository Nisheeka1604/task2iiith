import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, AirQuality, WaterQuality
import ast

# Database connection
DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def load_mapping(mapping_file):
    # Load the mapping file
    df_mapping = pd.read_csv(mapping_file)
    mapping = {}
    
    for _, row in df_mapping.iterrows():
        value_col = row['value_col']
        mapping[value_col] = ast.literal_eval(row['original_column'])
    
    return mapping

def import_data(data_file, mapping_file):
    # Load data and mapping
    df = pd.read_csv(data_file)
    mapping = load_mapping(mapping_file)
    
    # Create database session
    db = SessionLocal()
    
    # Create tables if they don't exist
    Base.metadata.create_all(bind=engine)
    
    # First, clear existing data to avoid duplicates
    db.query(AirQuality).delete()
    db.query(WaterQuality).delete()
    db.commit()
    
    # Process each row in the dataset
    for _, row in df.iterrows():
        try:
            node_id = row['node_id']
            node_type = row['type']
            
            if node_type == 'AQ':
                # Process Air Quality data
                aq_data = {
                    'node_id': node_id,
                    'pm2_5': row.get('value 1', None),
                    'pm10': row.get('value 3', None),
                    'temperature': row.get('value 5', None),
                    'relative_humidity': row.get('value 7', None),
                    'humidity': row.get('value 7', None),  # Using same as relative_humidity
                    'noise': row.get('value 9', None),
                    'co2': None  # Not in the dataset
                }
                
                # Add new record (we've already cleared existing data)
                db.add(AirQuality(**aq_data))
                
            elif node_type == 'WF':
                # For Water Flow data, we'll store it in the WaterQuality table
                # Map the fields as best as we can
                wq_data = {
                    'node_id': node_id,
                    'temperature': row.get('value 5', None),  # Using temperature if available
                    # Map other fields to the best matching columns
                    'tds': row.get('value 3', None),  # Using pressure as TDS (temporary)
                    'turbidity': row.get('value 1', None),  # Using flow rate as turbidity (temporary)
                    'ph': row.get('value 4', None)  # Using pressure_voltage as pH (temporary)
                }
                
                db.add(WaterQuality(**wq_data))
                
            # Commit after each record to handle errors individually
            db.commit()
                
        except Exception as e:
            print(f"Error processing row {_}: {e}")
            db.rollback()
    
    # Commit changes
    try:
        db.commit()
        print("Data imported successfully!")
    except Exception as e:
        db.rollback()
        print(f"Error importing data: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    import os
    
    # Get the directory of the current script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Construct paths to the data files
    data_file = os.path.join(os.path.expanduser("~"), "Downloads", "QuickShare_2511062335", "iot_dataset.csv")
    mapping_file = os.path.join(os.path.expanduser("~"), "Downloads", "QuickShare_2511062335", "iot_dataset_mapping.csv")
    
    # Import the data
    import_data(data_file, mapping_file)
