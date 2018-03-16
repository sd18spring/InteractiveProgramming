"""Hurricane.py contains the code for the Hurricane class, which is utilized in the Model class. Make sure to have
the numpy and datetime libraries. Script can be run just by typing "python Hurricane.py" in terminal."""
import numpy as np
from datetime import datetime
import pandas as pd


class Hurricane(object):
    """
    The Hurricane class represents each hurricane in the map. Id, name, latitude, longitude, season, times,
    and winds are extracted from a large data frame inputted by Model.py. Each hurricane object contains information
    necessary for the hover, slider, and plotting tools in Map.py.
    """

    def __init__(self, df):
        """
        Creates the hurricane object with a data frame obtained from NOAA. Each object has an id, name, a season,
        a date, a duration, a category, and arrays of web mercator projection coordinates.

        :param df: data frame that Model.__init__ creates, there is one df for each hurricane
        """
        self.id = df['Serial_Num'][1]
        self.name = df['Name'][1]

        lats = df['Latitude_for_mapping'][1:]
        longs = df['Longitude_for_mapping'][1:]
        self.x = self.convertLong(longs)
        self.y = self.convertLat(lats)

        self.season = df['Season'][1]
        times = df['ISO_time'][1:].tolist()

        self.time = self.findTime(self.season, times[0])
        self.duration = self.findDuration(times)

        winds = df['Wind(WMO)'][1:]
        winds = np.asfarray(winds.values, float)
        self.category = self.findCat(winds)

    def __str__(self):
        """
        Creates a string representation of a hurricane object
        :return: the string representing hurricane
        """
        output = "ID: " + str(self.id) + " Name: " + str(self.name) + " Time: " + str(self.time) + " Duration: " + \
                 str(self.duration) + " Cat: " + str(self.category) + "\n" + "\n" + "x:" + str(
            self.x) + "\n" + "y:" + str(self.y)
        return output

    def convertLong(self, longs):
        """
        Converts an array of longitudes signifying a hurricane's path to web mercator x values. This function was
        tested by plotting several hurricanes with known locations and then making sure they were plotted in the
        correct area.
        :param longs: data frame of longitudes of a hurricane path
        :return: an array of x coordinates to be plotted

        """
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
        """
        Converts an array of latitudes signifying a hurricane's path to web mercator y values. This function was
        tested by plotting several hurricanes with known locations and then making sure they were plotted in the
        correct area.
        :param lats: data frame of latitudes of a hurricane path
        :return: an array of y coordinates to be plotted
        """
        k = 6378137
        y = []
        for j in np.asfarray(lats.values, float):
            yj = np.log(np.tan((90 + j) * np.pi / 360.0)) * k
            y.append(yj)
        return y

    def findTime(self, season, time):
        """
        Takes the season (represents the year of the hurricane) and the first time value (used to get
        the month of hurricane) and combines them into one string for the hover tool
        :param season: str of the year of the hurricane
        :param time: time of first data point of the hurricane
        :return: str of year and month of hurricane
        """
        # array of month names that gets referenced
        months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
                  "November", "December"]
        # convert the month in "time" to an int and match it to the right month name
        month = int(time[5] + time[6]) - 1
        return season + ", " + months[month]

    def findDuration(self, times):
        """
        Takes an array of time values for a hurricane and calculates the time difference in days between the first and
        last point. Uses the python datetime library.
        :param times: array of time values
        :return: str representing duration of a hurricane in days
        """
        start = times[0][:10]
        end = times[len(times) - 1][:10]
        start2 = datetime.strptime(start, "%Y-%m-%d")
        end2 = datetime.strptime(end, "%Y-%m-%d")
        duration = abs((end2 - start2).days)
        return str(duration) + " day(s)"

    def findCat(self, winds):
        """
        Takes an array of maximum sustained wind values in knots and determines the maximum value.
        From the maximum value, the category is determined. The categories at 1 to 5, but there is also TS and TD
        and NA. (-999 is replaced with -1)
        :param winds: array of wind values
        :return: str representing the category
        """
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

if __name__ == '__main__':
    # TESTING: creates a hurricane object using the 12700th URL in CSVFiles.csv and then prints it
    df = pd.read_csv("CSVFiles.csv", low_memory=False)
    url = df.values[12700]
    url = "ftp://eclipse.ncdc.noaa.gov" + url[0]
    data = pd.read_csv(url)
    data.to_csv("hurricane.csv", header=None)
    df2 = pd.read_csv("hurricane.csv", low_memory=False)
    b = Hurricane(df2)
    print(b)
