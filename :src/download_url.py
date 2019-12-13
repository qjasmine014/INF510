import argparse
import requests
import ast
from datetime import datetime, timedelta
from bs4 import BeautifulSoup

def download_url1():

    headers = {"user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36",
               "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3"}
    for day in range(1, 90):
        file_name = (datetime.now() + timedelta(days=day)).strftime("%Y-%m-%d")
        url = 'https://www.accuweather.com/en/us/los-angeles/90012/daily-weather-forecast/347625?day=' + str(day)
        r = requests.get(url,headers=headers)
        with open(file_name+'.htm', 'w+b') as f:
            f.write(r.content)
    return


def download_url2():
    for month in range(1,13):
        if month < 10:
            file_name = '2012-0' + str(month)
        else:
            file_name = '2012-' + str(month)
        url_past = 'https://www.usclimatedata.com/climate/los-angeles/california/united-states/usca1339/2012/' + str(month)
        r_past = requests.get(url_past)
        with open(file_name+'.htm', 'w+b') as f:
            f.write(r_past.content)
    return


def download():
    download_url1()
    download_url2()
    return






