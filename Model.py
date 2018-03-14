"""Model.py contains the code for the Model class, which has Hurricane objects and is created in the View class.
Make sure to have Hurricane.py, pandas, and pickle. Script can be run just by typing "python Model.py" in terminal. """
from Hurricane import Hurricane
import pandas as pd
import pickle


class Model(object):
    """
    The Model class creates the Hurricane objects by reading in csv files stored in the NOAA FTP server. The links to
    the csv files are extracted from "data.py" and stored in the "CSVFiles.csv" (chronological order). The Hurricane
    objects are also stored in a pickle file, so objects do not need to be created each time the map is run.
    """
    # MAXNUM is the total number of hurricanes in the NOAA database
    MAXNUM = 12861

    def __init__(self, start=None, end=None):
        """
        Creates the hurricane objects given a start and end index for the "CSVFiles.csv" and stories the objects in
        an array. If no start is given, start is set to the index of the first hurricane. If no end if given,
        end is set to the index of the last hurricane.
        :param start: index of first hurricane to extract data from
        :param end: index of last hurricane to extract data from
        """
        self.hurricaneLst = []

        if start is None:
            start = 0

        if end is None:
            end = Model.MAXNUM

        # read in "CSVFiles.csv" and extract the data frames with the urls from start to end and call __init__ for
        # Hurricane class and append object to hurricane list attribute
        df = pd.read_csv("CSVFiles.csv", low_memory=False)
        for i in range(start, end):
            url = df.values[i]
            url = "ftp://eclipse.ncdc.noaa.gov" + url[0]
            data = pd.read_csv(url)
            data.to_csv("hurricane.csv", header=None)
            df2 = pd.read_csv("hurricane.csv", low_memory=False)
            hurricane = Hurricane(df2)
            self.hurricaneLst.append(hurricane)

    def __str__(self):
        """
        Creates a string representation of a model object by calling the Hurricane.__str__ for each hurricane in
        hurricaneLst
        :return: the string representing model
        """
        output = ""
        for elm in self.hurricaneLst:
            output += Hurricane.__str__(elm)
            output += "\n" + "\n"
        return output

    def pickle(self):
        """
        Iterates through hurricaneLst and dumps each hurricane object into one pickle file
        :return: nothing
        """
        with open('hurricane_data.pkl', 'wb') as output:
            pickle.dump(len(self.hurricaneLst), output)
            for elm in self.hurricaneLst:
                pickle.dump(elm, output)


if __name__ == '__main__':
    # TESTING, makes model object using first 100 hurricanes and then puts the data into a pickle file
    test = Model(0, 100)
    test.pickle()
    # print(test)
