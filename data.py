"""data.py uses data scrapping techniques to extract the links of the csv files for each hurricane in the NOAA
database. The script was only intended to be run once to generate CSVFiles.csv, which is used in Model.py. Make sure
to have the splinter, BeautifulSoup, time, and pandas libraries if you want to run/modify the script. To run the
script, just type "python data.py" in the terminal. If you have any questions feel free to send an email to
cassandra.overney@students.olin.edu """

from splinter import Browser
from bs4 import BeautifulSoup
from time import sleep
import pandas as pd

def get_CSVFiles():
    """
    Opens up a Chrome browser, navigates to the FTP server in NOAA and uses BeautifulSoup to extract all of the URLs
    from a table of hurricanes.
    :return: list of urls, one for each hurricane
    """
    urls = []
    # Opens up a Chrome browser, you may have to download a chrome driver and change the executable path accordingly
    executable_path = {'executable_path':'/bin/chromedriver'}
    browser = Browser('chrome', **executable_path)
    # vists the correct URL and extracts all the links from the HTML table file
    url = "ftp://eclipse.ncdc.noaa.gov/pub/ibtracs/v03r10/all/csv/storm/"
    browser.visit(url)
    sleep(15)
    soup = BeautifulSoup(browser.html, "html.parser")
    tab = soup.table
    # print(links[0:10])
    for a in tab.find_all('a', href=True):
        urls.append(a['href'])
    browser.quit()
    return urls

if __name__ == '__main__':
    # calls get_CSVFiles and turns the array of URLs into a data frame and then writes that data frame to a csv file.
    urls = get_CSVFiles()
    print(urls[0:10])
    df = pd.DataFrame(urls)
    df.to_csv("CSVFiles.csv", header=None, index=None)