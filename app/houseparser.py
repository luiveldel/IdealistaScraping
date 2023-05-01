import pandas as pd

class HouseDataParser:
    
    def __init__(self, data_json):
        self.df = pd.DataFrame.from_dict(data_json['elementList'])

    def parse_data(self):
        self.df = self.df[['price', 'size', 'rooms', 'bathrooms', 'district', 'neighborhood']].astype({"price":int,"size":int})

    def to_csv(self):
        self.df.to_csv('output/houses.csv', index=False)

    def to_excel(self):
        self.df.to_excel('output/houses.xlsx', index=False)