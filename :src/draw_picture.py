import matplotlib.pyplot as plt
import pandas as pd
from clean import clean_data

future_dates,past_dates_format = clean_data()

def future_picture(future_dates):
    # draw picture of future_temperature_from_url and future_temperature_from_api
    plt.style.use('ggplot')
    fig = plt.figure(figsize=(10, 6))
    colors1 = '#6D6D6D'

    data1 = pd.read_csv('future_temperature_from_url.csv')['Day Temperature'].values.tolist()
    for i in range(len(data1)):
        data1[i] = float(data1[i][:-1])
    data3 = pd.read_csv('future_temperature_from_url.csv')['Night Temperature'].values.tolist()
    for i in range(len(data1)):
        data3[i] = float(data3[i][:-1])

    data2 = pd.read_csv('future_temperature_from_api_cleaned.csv')['Day Temperature'].values.tolist()
    data4 = pd.read_csv('future_temperature_from_api_cleaned.csv')['Night Temperature'].values.tolist()

    plt.plot(future_dates, data1, label='day_temperature_url')
    plt.plot(future_dates, data2, label='day_temperature_api')
    plt.plot(future_dates, data3, label='night_temperature_url')
    plt.plot(future_dates, data4, label='night_temperature_api')
    plt.title('the difference of future temperature between url and api')
    plt.xlabel('date')
    plt.ylabel('temperature')
    plt.legend()
    plt.savefig('future_temperature.png', bbox_inches='tight', dpi=300)

def past_picture(past_dates_format):
    # draw picture of past_temperature_from_url and past_temperature_from_api
    plt.style.use('ggplot')
    fig = plt.figure(figsize=(10, 6))
    colors1 = '#6D6D6D'

    data1 = pd.read_csv('past_temperature_from_url.csv')['Past High Temperature'].values.tolist()
    for i in range(len(data1)):
        data1[i] = float(data1[i][:-1])
    data3 = pd.read_csv('past_temperature_from_url.csv')['Past Low Temperature'].values.tolist()
    for i in range(len(data1)):
        data3[i] = float(data3[i][:-1])

    data2 = pd.read_csv('past_temperature_from_api_cleaned.csv')['Past High Temperature'].values.tolist()
    data4 = pd.read_csv('past_temperature_from_api_cleaned.csv')['Past Low Temperature'].values.tolist()

    plt.plot(past_dates_format, data1, label='high_temperature_url')
    plt.plot(past_dates_format, data2, label='high_temperature_api')
    plt.plot(past_dates_format, data3, label='low_temperature_url')
    plt.plot(past_dates_format, data4, label='low_temperature_api')
    plt.title('the difference of past temperature between url and api')
    plt.xlabel('date')
    plt.ylabel('temperature')
    plt.legend()
    plt.savefig('past_temperature.png', bbox_inches='tight', dpi=300)

def draw_picuture(future_dates,past_dates_format):
    future_picture(future_dates)
    past_picture(past_dates_format)
    return
