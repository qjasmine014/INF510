import pandas as pd

def clean_data():
    '''
    Since the data of the api is 24 hours, I hope it is more like the data of the url.
    :return:
    '''
    # future temperatures from api are converted to day and night temperature

    future_temperature_from_api = pd.read_csv('future_temperature_from_api.csv')
    day_temperature_list = list()
    night_temperature_list = list()
    future_dates =list()
    for i in range(len(future_temperature_from_api.values)):
        day_temperature = 0
        night_temperature = 0
        the_number_day = 0
        the_number_night = 0
        for j in range(1, len(future_temperature_from_api.values[i])):
            if future_temperature_from_api.values[i][j] != 'None':
                if j < 9:
                    night_temperature += float(future_temperature_from_api.values[i][j][:-1])
                    the_number_night += 1
                else:
                    day_temperature += float(future_temperature_from_api.values[i][j][:-1])
                    the_number_day += 1
        day_temperature_list.append(round(day_temperature / the_number_day, 2))
        night_temperature_list.append(round(night_temperature / the_number_night, 2))
        future_dates.append(future_temperature_from_api.values[i][0])
    data = {'Day Temperature': day_temperature_list, 'Night Temperature': night_temperature_list}
    dataframe_future = pd.DataFrame(data, index=future_dates)
    dataframe_future.to_csv("future_temperature_from_api_cleaned.csv", index=True, sep=',')

    # past temperatures from api are converted to high and low temperature
    past_temperature_from_api = pd.read_csv('past_temperature_from_api.csv')
    high_temperature_list = list()
    low_temperature_list = list()
    past_dates_format = list()
    for i in range(len(past_temperature_from_api.values)):
        temperature_list = list()
        for j in range(1, len(past_temperature_from_api.values[i])):
            if past_temperature_from_api.values[i][j] != 'None':
                temperature_list.append(float(past_temperature_from_api.values[i][j][:-1]))
        high_temperature_list.append(max(temperature_list))
        low_temperature_list.append(min(temperature_list))
        past_dates_format.append(past_temperature_from_api.values[i][0])
    past_data = {'Past High Temperature': high_temperature_list, 'Past Low Temperature': low_temperature_list}
    dataframe_past = pd.DataFrame(past_data, index=past_dates_format)
    dataframe_past.to_csv("past_temperature_from_api_cleaned.csv", index=True, sep=',')
    return future_dates,past_dates_format















