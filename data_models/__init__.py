import csv
import os
from dotenv import load_dotenv

from tqdm import tqdm
from sqlalchemy import create_engine, ForeignKey, Column, String, Integer, CHAR, Float, Index
from sqlalchemy.orm import sessionmaker
from data_models.DataModel import DataModel
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

import data_models.AirQualitySummary
import data_models.GovermentBudgetSurplus

load_dotenv()

# Returns database session
def setup_database():
    # Define the connection string
    username = os.getenv('DB_USER')
    password = os.getenv('DB_PASSWORD')
    host = os.getenv('DB_HOST')
    port = os.getenv('DB_PORT')  # Optional, default is 5432 for PostgreSQL
    database = os.getenv('DB_DATABASE')

    # Format the connection string
    connection_string = os.getenv('DB_URL') or f'postgresql://{username}:{password}@{host}:{port}/{database}'
    engine = create_engine(connection_string)

    Base.metadata.create_all(engine)
    return sessionmaker(bind=engine)()
