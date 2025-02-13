from typing import override

from data_models import *
from data_sources.Eurostat import Eurostat
from math import isnan


class GovermentBudgetSurplus(Base, DataModel):
    __tablename__ = 'gov_budget_surplus'

    id = Column(Integer, primary_key=True)
    year = Column('year', Integer)
    country_name = Column('country_name', String)
    budget_surplus = Column('budget_surplus', Float)

    def __init__(self, year, country_name, budget_surplus):
        self.year = year
        self.country_name = country_name
        self.budget_surplus = budget_surplus

    @staticmethod
    def load_all(database_session):
        GovermentBudgetSurplus.load_from_eurostat(database_session)

    @staticmethod
    def load_from_eurostat(db_session):
        print('Calling Eurostat...')
        dataset = Eurostat.gov_deficit_surplus()

        print('Reading response...')
        df = dataset.write('dataframe')
        loaded_entries = []
        total_lines = len(df)

        print(f"Reading {total_lines} bytes of data...")
        for index, row in df.iterrows():
            country = row['Geopolitical entity (reporting)']
            year = row['Time']
            value = row['value']

            if not isnan(value):
                loaded_entries.append(GovermentBudgetSurplus(year, country, value))

        GovermentBudgetSurplus.reset_database_to(loaded_entries, db_session)

        print('Done!')

if __name__ == '__main__':
    new_database_session = setup_database()
    GovermentBudgetSurplus.load_from_eurostat(new_database_session)