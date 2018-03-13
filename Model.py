from Hurricane import Hurricane
import pandas as pd
import pickle


class Model(object):
    MAXNUM = 12861

    def __init__(self, start=None, end=None):
        # make the Hurricanes
        self.hurricaneLst = []
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
            self.hurricaneLst.append(hurricane)

        # make view and Bokeh stuff

    def __str__(self):
        output = ""
        for elm in self.hurricaneLst:
            output += Hurricane.__str__(elm)
            output += "\n" + "\n"
        return output

    def pickle(self):
        with open('hurricane_data.pkl', 'wb') as output:
            pickle.dump(len(self.hurricaneLst),output)
            for elm in self.hurricaneLst:
                pickle.dump(elm, output)


# TESTING
test = Model(0, 100)
test.pickle()
# print(test)
