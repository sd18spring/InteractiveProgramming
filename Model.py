from Hurricane import Hurricane
from collections import defaultdict
import pandas as pd


class Model(object):
    MAXNUM = 12861

    def __init__(self, start=None, end=None):
        # make the Hurricanes
        self.hurricaneLst = defaultdict(list)
        if start is None:
            start = 0
        if end is None:
            end = Model.MAXNUM
        for i in range(start, end):
            df = pd.read_csv("CSVFiles.csv", low_memory=False)
            url = df.values[i]
            url = "ftp://eclipse.ncdc.noaa.gov" + url[0]
            data = pd.read_csv(url)
            data.to_csv("hurricane.csv", header=None)
            df2 = pd.read_csv("hurricane.csv", low_memory=False)
            hurricane = Hurricane(df2)
            self.hurricaneLst[int(hurricane.season)].append(hurricane)

        # make view and Bokeh stuff

    def __str__(self):
        output = ""
        for k, v in self.hurricaneLst.items():
            output += "YEAR: " + str(k) + "\n"
            for elm in v:
                output += Hurricane.__str__(elm)
            output += "\n" + "\n"
        return output


# TESTING
test = Model(0, 5)
print(test)
