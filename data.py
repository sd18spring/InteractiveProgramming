# Imports the necessary libraries and creates the arrays needed to store information from NOAA
# You have to make sure that you have the splinter and BeautifulSoup libraries
from splinter import Browser
from bs4 import BeautifulSoup
from time import sleep
import pandas as pd

def get_CSVFiles():
    urls = []
    # Opens up a Chrome browser
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
    urls = get_CSVFiles()
    print(urls[0:10])
    df = pd.DataFrame(urls)
    df.to_csv("CSVFiles.csv", header=None, index=None)