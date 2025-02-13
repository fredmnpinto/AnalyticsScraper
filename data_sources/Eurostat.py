from math import isnan

from pyjstat import pyjstat

class Eurostat:
    HOST_URL = 'https://ec.europa.eu/eurostat/api/dissemination'

    @staticmethod
    def request(dataset: str):
        return pyjstat.Dataset.read(f"{Eurostat.HOST_URL}/statistics/1.0/data/{dataset}")

    @staticmethod
    def gov_deficit_surplus():
        return Eurostat.request(dataset='gov_10dd_edpt1')


if __name__ == '__main__':
    dataset = Eurostat.gov_deficit_surplus()

    df = dataset.write('dataframe')

    for index, row in df.iterrows():
        country = row[4]
        year = row[5]
        value = row[6]

        if not isnan(value):
            print(country, year, value)
