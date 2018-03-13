from Hurricane import Hurricane
from collections import defaultdict
import pandas as pd
import pickle


class Model(object):
    MAXNUM = 12861

    def __init__(self, start=None, end=None):
        # make the Hurricanes
        self.hurricaneLst = defaultdict(list) # might want to change to just a simple array
        if start is None:
            start = 0
        if end is None:
            end = Model.MAXNUM

        df = pd.read_csv("CSVFiles.csv", low_memory=False)
        for i in range(start, end):
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

    def pickle(self):
        with open('hurricane_data.pkl', 'wb') as output:
            for k, v in self.hurricaneLst.items():
                for elm in v:
                    pickle.dump(elm, output, pickle.HIGHEST_PROTOCOL)


# TESTING
test = Model(12000, 12100)
test.pickle()
# print(test)
