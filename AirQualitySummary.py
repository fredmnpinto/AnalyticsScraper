# From WHO yearly summary database
class AirQualitySummary(object):
    TOKEN = 'z425xazht0wtjth8onxxyhh2ea2qccfc67opv2vk'
    def __init__(
            self,
            year,
            city,
            country,
            pm10_concentration,
            pm25_concentration,
            no2_concentration,
            pm10_tempcov,
            pm25_tempcov,
            no2_tempcov
    ):
        self.year = year
        self.city = city
        self.country = country
        self.pm10_concentration = pm10_concentration
        self.pm25_concentration = pm25_concentration
        self.no2_concentration = no2_concentration
        self.pm10_tempcov = pm10_tempcov
        self.pm25_tempcov = pm25_tempcov
        self.no2_tempcov = no2_tempcov

    @staticmethod
    def extract_from_csv(file_path: str):
        