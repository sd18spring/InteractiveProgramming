import pandas as pd


class Hurricane(object):
    # Primary constructor
    def __init__(self, df):
        self.id = df['Serial_Num'][1]
        self.lats = df['Latitude_for_mapping'][1:]  # you can also use df['column_name']
        self.longs = df['Longitude_for_mapping'][1:]
        self.season = df['Season'][1]
        self.name = df['Name'][1]
        self.times = df['ISO_time'][1:]
        self.natures = df['Nature'][1:]
        self.winds = df['Wind(WMO)'][1:]

    def __str__(self):
        output = "ID: " + self.id + " Name: " + self.name + " Season: " + self.season + "\n" + "Longs: " + str(
            self.longs) + "\n" + "Lats: " + str(self.lats)
        return output

# TESTING
# df = pd.read_csv("CSVFiles.csv", low_memory=False)
# url = df.values[0]
# url = "ftp://eclipse.ncdc.noaa.gov" + url[0]
# data = pd.read_csv(url)
# data.to_csv("hurricane.csv", header=None)
# df2 = pd.read_csv("hurricane.csv", low_memory=False)
# b = Hurricane(df2)
# print(b)
