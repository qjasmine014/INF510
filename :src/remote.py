import argparse
import requests
import pandas as pd
import ast
from datetime import datetime, timedelta
from bs4 import BeautifulSoup

def request_soup(day):
    '''
    Get soup from url: https://www.accuweather.com/en/us/los-angeles/90012/daily-weather-forecast/347625?day=
    This website can predict day and night temperatures for the next 90 days

    :param day: the difference between predicted date and current date
    :return:
    '''
    headers = {"user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36",
               "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3"}
    url = 'https://www.accuweather.com/en/us/los-angeles/90012/daily-weather-forecast/347625?day=' + str(day)
    r = requests.get(url,headers=headers)
    soup = BeautifulSoup(r.content, 'lxml')
    return soup

def get_data_of_future(future_dates,future_day_temperatures,future_night_temperatures):
    '''

    :param future_date: empty list after initialization
    :param future_day_temperature: empty list after initialization
    :param future_night_temperature: empty list after initialization
    :return: future_date: predicted day
             future_day_temperature: day temperature recorded by the website
             future_night_temperature: night temperature recorded by the website
    '''
    for day in range(1,90):
        soup = request_soup(day+1)
        future_dates.append((datetime.now() + timedelta(days=day)).strftime("%Y-%m-%d"))
        future_day_temperatures.append(soup.find_all('p','value')[0].contents[0][5:8])
        future_night_temperatures.append(soup.find_all('p','value')[1].contents[0][5:8])
    return future_dates,future_day_temperatures,future_night_temperatures

def get_data_of_future_by_api(future_dates,future_temperature_for_24_hours):
    '''

    :param all dates where temperature needs to be predicted
    :param temperature_for_24_hours:
    :return: dictionary storage : {hour: temperature_of_day_1,temperature_of_day_2,temperature_of_day_2}
    '''
    key = 'a6ef1d33dfca336bec962d061cd02e6d'
    # the longitude and latitude in Los Angeles
    latitude = '34.0522'
    longitude = '-118.2437'
    data_api = list()
    for date in future_dates:
        time = date + 'T12:00:00'
        url_api = 'https://api.darksky.net/forecast/' + key + '/' + latitude + ',' + longitude + ',' + time
        data_api.append(requests.get(url_api).content)
    for i in range(len(data_api)):
        hour_temperature = ast.literal_eval(data_api[i].decode('utf-8'))['hourly']['data'][0:24]
        for hour_status in hour_temperature:
            if str(datetime.fromtimestamp(hour_status['time']))[11:16] not in future_temperature_for_24_hours:
                future_temperature_for_24_hours[str(datetime.fromtimestamp(hour_status['time']))[11:16]] = [str(hour_status['temperature'])+'°']
            else:
                future_temperature_for_24_hours[str(datetime.fromtimestamp(hour_status['time']))[11:16]].append(str(hour_status['temperature'])+'°')
        for key, value in future_temperature_for_24_hours.items():
            m = len(value)
            while m < (i + 1):
                future_temperature_for_24_hours[key].append('None')
                m += 1
            while m > (i + 1):
                future_temperature_for_24_hours[key].pop()
                m -= 1
    return future_temperature_for_24_hours

def request_past_soup(year,month):
    '''
    Get soup from url: https://www.usclimatedata.com/climate/los-angeles/california/united-states/usca1339/
    This website can get the highest and lowest temperature of a past day

    :param year: one past year
    :param month: one past month
    :return:
    '''
    url_past = 'https://www.usclimatedata.com/climate/los-angeles/california/united-states/usca1339/'+ str(year) + '/' + str(month)
    r_past = requests.get(url_past)
    soup_past = BeautifulSoup(r_past.content, 'lxml')
    return soup_past

def get_past_data(past_dates,past_high_temperatures,past_low_temperatures):
    '''

    :param past_dates: empty list after initialization
    :param past_high_temperatures: empty list after initialization
    :param past_low_temperatures: empty list after initialization
    :return:
    '''
    for month in range(1,13):
        soup_past = request_past_soup(2012,month)
        history = soup_past.find_all(id='history')[0]
        if month == 1 or month == 3 or month == 5 or month == 7 or month == 8 or month == 10 or month == 12:
            for i in range(0,186,6):
                past_dates.append(history.find_all('td')[i].contents[0])
                past_high_temperatures.append(history.find_all('td')[i+1].contents[0]+'°')
                past_low_temperatures.append(history.find_all('td')[i+2].contents[0]+'°')
        elif month == 4 or month == 6 or month == 9 or month == 11:
            for i in range(0,180,6):
                past_dates.append(history.find_all('td')[i].contents[0])
                past_high_temperatures.append(history.find_all('td')[i+1].contents[0]+'°')
                past_low_temperatures.append(history.find_all('td')[i+2].contents[0]+'°')
        else:
            for i in range(0,168,6):
                past_dates.append(history.find_all('td')[i].contents[0])
                past_high_temperatures.append(history.find_all('td')[i+1].contents[0]+'°')
                past_low_temperatures.append(history.find_all('td')[i+2].contents[0]+'°')
    return past_dates,past_high_temperatures,past_low_temperatures

def get_past_data_from_api(past_dates_format,past_temperature_for_24_hours):
    '''

    :param past_date_format: standard form of past date
    :return: dictionary storage : {hour: temperature_of_day_1,temperature_of_day_2,temperature_of_day_2}
    '''
    key = 'a6ef1d33dfca336bec962d061cd02e6d'
    # the longitude and latitude in Los Angeles
    latitude = '34.0522'
    longitude = '-118.2437'
    data_api_for_past = list()
    for date in past_dates_format:
        past_time = date + 'T12:00:00'
        url_api_for_past = 'https://api.darksky.net/forecast/' + key + '/' + latitude + ',' + longitude + ',' + past_time
        data_api_for_past.append(requests.get(url_api_for_past).content)
    for i in range(len(data_api_for_past)) :
        hour_temperature = ast.literal_eval(data_api_for_past[i].decode('utf-8'))['hourly']['data'][0:24]
        for hour_status_past in hour_temperature:
            if str(datetime.fromtimestamp(hour_status_past['time']))[11:16] not in past_temperature_for_24_hours:
                past_temperature_for_24_hours[str(datetime.fromtimestamp(hour_status_past['time']))[11:16]] = [str(hour_status_past['temperature']) + '°']
            else:
                past_temperature_for_24_hours[str(datetime.fromtimestamp(hour_status_past['time']))[11:16]].append(str(hour_status_past['temperature']) + '°')
        for key, value in past_temperature_for_24_hours.items():
            m = len(value)
            while m < (i + 1):
                past_temperature_for_24_hours[key].append('None')
                m += 1
            while m > (i + 1):
                past_temperature_for_24_hours[key].pop()
                m -= 1
    return past_temperature_for_24_hours


def grab_data_by_scraping_and_api_requests():
    # get data from the first url: future temperature
    future_dates = list()
    future_day_temperatures = list()
    future_night_temperatures = list()
    future_dates, future_day_temperatures, future_night_temperatures = get_data_of_future(future_dates, future_day_temperatures, future_night_temperatures)
    # store data as csv
    data = {'Day Temperature': future_day_temperatures, 'Night Temperature': future_night_temperatures}
    dataframe_future = pd.DataFrame(data, index=future_dates)
    dataframe_future.to_csv("future_temperature_from_url.csv", index=True, sep=',')

    # get data from the api: future temperature
    future_temperature_for_24_hours = dict()
    future_temperature_for_24_hours = get_data_of_future_by_api(future_dates, future_temperature_for_24_hours)
    # store data as csv
    dataframe_api_future = pd.DataFrame(future_temperature_for_24_hours, index=future_dates)
    dataframe_api_future.to_csv("future_temperature_from_api.csv", index=True, sep=',')

    # get data from the first url: past temperature
    past_dates = list()
    past_high_temperatures = list()
    past_low_temperatures = list()
    past_dates, past_high_temperatures, past_low_temperatures = get_past_data(past_dates, past_high_temperatures,past_low_temperatures)
    # store data as csv
    months = {'jan': '01', 'feb': '02', 'mar': '03', 'apr': '04', 'may': '05', 'jun': '06', 'jul': '07', 'aug': '08',
              'sep': '09', 'oct': '10', 'nov': '11', 'dec': '12'}
    past_dates_format = list()
    for i in range(0, 365):
        if 0 < int(past_dates[i].split()[0]) < 10:
            past_dates_format.append(
                past_dates[i].split()[2] + '-' + months[past_dates[i].split()[1]] + '-0' + past_dates[i].split()[0])
        else:
            past_dates_format.append(
                past_dates[i].split()[2] + '-' + months[past_dates[i].split()[1]] + '-' + past_dates[i].split()[0])
    past_data = {'Past High Temperature': past_high_temperatures, 'Past Low Temperature': past_low_temperatures}
    dataframe_past = pd.DataFrame(past_data, index=past_dates_format)
    dataframe_past.to_csv("past_temperature_from_url.csv", index=True, sep=',')

    # get data from the api: future temperature
    past_temperature_for_24_hours = dict()
    past_temperature_for_24_hours = get_past_data_from_api(past_dates_format,past_temperature_for_24_hours)
    # store data as csv
    dataframe_api_past = pd.DataFrame(past_temperature_for_24_hours, index=past_dates_format)
    dataframe_api_past.to_csv("past_temperature_from_api.csv", index=True, sep=',')

    return future_dates,past_dates_format





