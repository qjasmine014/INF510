import argparse
import requests
import pandas as pd
import ast
from datetime import datetime, timedelta
from bs4 import BeautifulSoup

def get_data_of_future(future_dates,future_day_temperatures,future_night_temperatures):
    '''

    :param future_date: empty list after initialization
    :param future_day_temperature: empty list after initialization
    :param future_night_temperature: empty list after initialization
    :return: future_date: predicted day
             future_day_temperature: day temperature recorded by the website
             future_night_temperature: night temperature recorded by the website
    '''
    for day in range(1, 90):
        file_name = (datetime.now() + timedelta(days=day)).strftime("%Y-%m-%d")
        with open(file_name +'.htm', 'r')as wb_data:
            soup = BeautifulSoup(wb_data, 'lxml')
            future_dates.append(file_name)
            future_day_temperatures.append(soup.find_all('p','value')[0].contents[0][5:8])
            future_night_temperatures.append(soup.find_all('p','value')[1].contents[0][5:8])
    return future_dates,future_day_temperatures,future_night_temperatures


def get_past_data(past_dates,past_high_temperatures,past_low_temperatures):
    '''

    :param past_dates: empty list after initialization
    :param past_high_temperatures: empty list after initialization
    :param past_low_temperatures: empty list after initialization
    :return:
    '''
    for month in range(1,13):
        if month < 10:
            file_name = '2012-0' + str(month)
        else:
            file_name = '2012-' + str(month)
        with open(file_name +'.htm', 'r')as wb_data:
            soup_past = BeautifulSoup(wb_data, 'lxml')
            history = soup_past.find_all(id='history')[0]
            if month == 1 or month == 3 or month == 5 or month == 7 or month == 8 or month == 10 or month == 12:
                for i in range(0, 186, 6):
                    past_dates.append(history.find_all('td')[i].contents[0])
                    past_high_temperatures.append(history.find_all('td')[i + 1].contents[0] + '°')
                    past_low_temperatures.append(history.find_all('td')[i + 2].contents[0] + '°')
            elif month == 4 or month == 6 or month == 9 or month == 11:
                for i in range(0, 180, 6):
                    past_dates.append(history.find_all('td')[i].contents[0])
                    past_high_temperatures.append(history.find_all('td')[i + 1].contents[0] + '°')
                    past_low_temperatures.append(history.find_all('td')[i + 2].contents[0] + '°')
            else:
                for i in range(0, 168, 6):
                    past_dates.append(history.find_all('td')[i].contents[0])
                    past_high_temperatures.append(history.find_all('td')[i + 1].contents[0] + '°')
                    past_low_temperatures.append(history.find_all('td')[i + 2].contents[0] + '°')

    return past_dates,past_high_temperatures,past_low_temperatures




def grab_data_from_downloaded_raw_files():
    # get data from the first url: future temperature
    future_dates = list()
    future_day_temperatures = list()
    future_night_temperatures = list()
    future_dates, future_day_temperatures, future_night_temperatures = get_data_of_future(future_dates, future_day_temperatures, future_night_temperatures)
    # store data as csv
    data = {'Day Temperature': future_day_temperatures, 'Night Temperature': future_night_temperatures}
    dataframe_future = pd.DataFrame(data, index=future_dates)
    dataframe_future.to_csv("future_temperature_from_url.csv", index=True, sep=',')

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

