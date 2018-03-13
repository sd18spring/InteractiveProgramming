import pandas as pd
import numpy as np
from datetime import datetime


class Hurricane(object):
    # Primary constructor
    def __init__(self, df):
        self.id = df['Serial_Num'][1]
        self.name = df['Name'][1]

        lats = df['Latitude_for_mapping'][1:]
        longs = df['Longitude_for_mapping'][1:]
        self.x = self.convertLong(longs)
        self.y = self.convertLat(lats)

        season = df['Season'][1]
        times = df['ISO_time'][1:].tolist()

        self.time = self.findTime(season, times[0])
        self.duration = self.findDuration(times)

        winds = df['Wind(WMO)'][1:]
        winds = np.asfarray(winds.values, float)
        self.category = self.findCat(winds)

    def __str__(self):
        output = "ID: " + str(self.id) + " Name: " + str(self.name) + " Time: " + str(self.time) + " Duration: " + \
                 str(self.duration) + " Cat: " + str(self.category) + "\n" + "\n" + "x:" + str(self.x) + "\n" + "y:" + str(self.y)
        return output

    def convertLong(self, longs):
        k = 6378137
        x = []
        for ind, i in enumerate(np.asfarray(longs.values, float)):
            # print('i type is: ', type(i))
            xi = i * (k * np.pi / 180.0)
            if ind > 0:
                if abs(xi - x[ind - 1]) > (10 ** 7):
                    xi = xi * -1
            x.append(xi)
        return x

    def convertLat(self, lats):
        k = 6378137
        y = []
        for j in np.asfarray(lats.values, float):
            yj = np.log(np.tan((90 + j) * np.pi / 360.0)) * k
            y.append(yj)
        return y

    def findTime(self, season, time):
        months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
                  "November", "December"]
        month = int(time[5] + time[6]) - 1
        return season + ", " + months[month]

    def findDuration(self, times):
        start = times[0][:10]
        end = times[len(times) - 1][:10]
        start2 = datetime.strptime(start, "%Y-%m-%d")
        end2 = datetime.strptime(end, "%Y-%m-%d")
        duration = abs((end2 - start2).days)
        return str(duration)

    def findCat(self, winds):
        maxWind = -1
        for wind in winds:
            if wind is -999:
                wind = -1
            if wind > maxWind:
                maxWind = wind

        if maxWind is -1:
            category = "NA"
        elif maxWind >= 137:
            category = "5"
        elif maxWind >= 113:
            category = "4"
        elif maxWind >= 96:
            category = "3"
        elif maxWind >= 83:
            category = "2"
        elif maxWind >= 64:
            category = "1"
        elif maxWind >= 34:
            category = "TS"
        else:
            category = "TD"

        return category


# TESTING
# df = pd.read_csv("CSVFiles.csv", low_memory=False)
# url = df.values[12700]
# url = "ftp://eclipse.ncdc.noaa.gov" + url[0]
# data = pd.read_csv(url)
# data.to_csv("hurricane.csv", header=None)
# df2 = pd.read_csv("hurricane.csv", low_memory=False)
# b = Hurricane(df2)
# print(b)
