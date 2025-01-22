import csv
import os
from dotenv import load_dotenv

from tqdm import tqdm
from sqlalchemy import create_engine, ForeignKey, Column, String, Integer, CHAR, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


# From WHO yearly summary database
class AirQualitySummary(Base):
    __tablename__ = 'air_quality_summaries'

    id = Column(Integer, primary_key=True)
    year = Column('year', Integer)
    city = Column('city', String)
    country_name = Column('country_name', String)
    pm10_concentration = Column('pm10_concentration', Float)
    pm25_concentration = Column('pm25_concentration', Float)
    no2_concentration = Column('no2_concentration', Float)
    pm10_tempcov = Column('pm10_tempcov', Float)
    pm25_tempcov = Column('pm25_tempcov', Float)
    no2_tempcov = Column('no2_tempcov', Float)

    def __init__(
            self,
            year,
            city,
            country_name,
            pm10_concentration,
            pm25_concentration,
            no2_concentration,
            pm10_tempcov,
            pm25_tempcov,
            no2_tempcov
    ):
        self.year = year
        self.city = city
        self.country_name = country_name
        self.pm10_concentration = pm10_concentration
        self.pm25_concentration = pm25_concentration
        self.no2_concentration = no2_concentration
        self.pm10_tempcov = pm10_tempcov
        self.pm25_tempcov = pm25_tempcov
        self.no2_tempcov = no2_tempcov

    @staticmethod
    def extract_from_csv(file_path: str, db_session):
        with open(file_path, encoding='utf-8') as csv_file:
            lines = len(csv_file.readlines())
            csv_data = csv.DictReader(csv_file)

            csv_file.seek(0)

            new_summaries = []

            for row in tqdm(csv_data, total=lines, desc="Reading data"):
                for key in row:
                    if row[key] == 'NA':
                        row[key] = None

                new_summaries.append(
                    AirQualitySummary(
                    row['year'],
                    row['city'],
                    row['country_name'],
                    row['pm10_concentration'].replace('.', '').replace(',', '.') if row['pm10_concentration'] is not None else None,
                    row['pm25_concentration'].replace('.', '').replace(',', '.') if row['pm25_concentration'] is not None else None,
                    row['no2_concentration'].replace('.', '').replace(',', '.') if row['no2_concentration'] is not None else None,
                    row['pm10_tempcov'].replace('.', '').replace(',', '.') if row['pm10_tempcov'] is not None else None,
                    row['pm25_tempcov'].replace('.', '').replace(',', '.') if row['pm25_tempcov'] is not None else None,
                    row['no2_tempcov'].replace('.', '').replace(',', '.') if row['no2_tempcov'] is not None else None)
                )

            print("Writting new data to database...")
            db_session.add_all(new_summaries)
            db_session.commit()
            print("Done!")

if __name__ == "__main__":
    load_dotenv()

    engine = create_engine(os.environ['DATABASE_URL'])
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)

    AirQualitySummary.extract_from_csv('data/who_air_quality_version_2024.csv', Session())
