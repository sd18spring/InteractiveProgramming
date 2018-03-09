import pandas as pd
import numpy as np


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
        self.x = self.convertlong()
        self.y = self.convertlat()

    def __str__(self):
        output = "ID: " + self.id + " Name: " + self.name + " Season: " + self.season + "\n" + "Longs: " + str(
            self.longs) + "\n" + "Lats: " + str(self.lats) + "\n" + "x:" + str(self.x) + "\n" + "y:" + str(self.y)
        return output

    def convertlong(self):
        k = 6378137
        x = []
        for i in np.asfarray(self.longs.values, float):
            # print('i type is: ', type(i))
            xi = i * (k * np.pi/180.0)
            x.append(xi)
        return x

    def convertlat(self):
        k = 6378137
        y = []
        for j in np.asfarray(self.lats.values, float):
            yj = np.log(np.tan((90 + j) * np.pi/360.0)) * k
            y.append(yj)
        return y

# TESTING
# df = pd.read_csv("CSVFiles.csv", low_memory=False)
# url = df.values[0]
# url = "ftp://eclipse.ncdc.noaa.gov" + url[0]
# data = pd.read_csv(url)
# data.to_csv("hurricane.csv", header=None)
# df2 = pd.read_csv("hurricane.csv", low_memory=False)
# b = Hurricane(df2)
# print(b)
