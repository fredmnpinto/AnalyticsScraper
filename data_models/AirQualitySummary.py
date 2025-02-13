from data_models import *

# From WHO yearly summary database
class AirQualitySummary(Base, DataModel):
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

    CSV_LOCATION = 'data_sources/csv/who_air_quality_version_2024.csv'

    __table_args__ = (
        Index('ix_summary_country_name_year_city', 'country_name', 'year', 'city', unique=True),  # Unique index
    )

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
    def load_all(database_session):
        AirQualitySummary.load_from_csv(AirQualitySummary.CSV_LOCATION, database_session)

    @staticmethod
    def load_from_csv(file_path: str, db_session):
        with open(file_path, encoding='utf-8') as csv_file:
            lines = len(csv_file.readlines())
            csv_data = csv.DictReader(csv_file)

            csv_file.seek(0)

            loaded_entries = []

            print(f"Reading {lines} lines of data...")
            for row in csv_data:
                for key in row:
                    if row[key] == 'NA':
                        row[key] = None

                loaded_entries.append(
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

            print("Writting to database...")
            AirQualitySummary.write_to_database(loaded_entries, db_session)
            print("Done!")

if __name__ == "__main__":
    new_database_session = setup_database()
    AirQualitySummary.load_from_csv(AirQualitySummary.CSV_LOCATION, new_database_session)
