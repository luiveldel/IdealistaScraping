import pandas as pd
from typing import Tuple

FIELDS_TO_EXTRACT: Tuple = ('price','size', 'rooms', 'bathrooms', 'district', 'neighborhood')

class HouseDataParser:

    df: pd.DataFrame
    
    def __init__(self, data_json):
        self.df = pd.DataFrame.from_dict(data_json['elementList'])

    def parse_data(self):
        self.df = self.df[FIELDS_TO_EXTRACT].astype({"price":int,"size":int})

    def to_csv(self):
        self.df.to_csv('output/houses.csv', index=False)

    def to_excel(self):
        self.df.to_excel('output/houses.xlsx', index=False)