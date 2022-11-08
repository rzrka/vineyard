import requests

import datetime
import time

from statistics import mean

LAT, LNG = 45.247136, 34.191395  # стартовые координаты
STEP_DIST = 0.000039  # шаг в градусах
MAX_SIZE_X, MAX_SIZE_Y = (1000, 1000)  # размер карты

OPENWEATHER_API = 'bce77f6c2965bbb5b4b5a7281fc5971f'
AGROMONITORING_API = '044c7d4cade46c7e721d5d149bd087c4'

# Временной промежуток за которой берутся данные
START_DATE = int(time.mktime(datetime.datetime.strptime('2022-07-01', "%Y-%m-%d").timetuple()))
END_DATE = int(time.mktime(datetime.datetime.strptime('2022-07-08', "%Y-%m-%d").timetuple()))


def weather_dataset(lat, lng):
    """
    Получение почвеных данных
    :param lat: float, широта
    :param lng: float, долгота
    :return: dict
        """
    url = f"https://history.openweathermap.org/data/2.5/history/city?lat={lat}&lon={lng}&type=hour&start={START_DATE}&end={END_DATE}&appid={OPENWEATHER_API}"
    dataset = {}
    response = requests.get(url)
    data = response.json()['list']
    dataset['temp'] = round(mean([x['main']['temp'] - 273.15 for x in data]), 2)  # Температура
    dataset['pressure'] = round(mean([x['main']['pressure'] for x in data]), 2)  # Давление
    dataset['humidity'] = round(mean([x['main']['humidity'] for x in data]), 2)  # Влажность
    dataset['wind_speed'] = round(mean([x['wind']['speed'] for x in data]), 2)  # Скорость ветра
    dataset['wind_gust'] = round(mean([x['wind']['gust'] for x in data]), 2)  # порыв ветра
    dataset['clouds'] = round(mean([x['clouds']['all'] for x in data]), 2)  # облачность, %
    dataset['weather'] = {''.join(tuple(l['description'] for l in j)) for j in
                          [i['weather'] for i in data]}  # облачность, %
    return dataset


def soil_dataset(lat, lng):
    """
    Получение почвеных данных
    :param lat: float, широта
    :param lng: float, долгота
    :return: dict
    """
    query_params = {'lat': lat, "lon": lng}

    REST_URL = "https://rest.isric.org"
    prop_query_url = f"{REST_URL}/soilgrids/v2.0/properties/query"

    response = requests.get(prop_query_url, params={**query_params, })
    data = response.json()
    data_set = {}
    for layer in data['properties']['layers']:
        soil_data = {layer['name']: {}}
        for value in layer['depths']:
            soil_data[layer['name']][value['label']] = value['values']
        data_set |= soil_data

    return data_set


def create_polygons(slat, slng):
    polygons = {}
    step = int(STEP_DIST * 1000000 * 2)
    start_lat = int(slat * 1000000)
    start_lng = int(slng * 1000000)
    stop_lat = start_lat + int(step * MAX_SIZE_Y)
    stop_lng = start_lng + int(step * MAX_SIZE_X)
    for lat in range(start_lat, stop_lat, step):
        lat /= 1000000
        for lng in range(start_lng, stop_lng, step):
            lng /= 1000000
            polygons[(lat, lng)] = {
                'x1': lng - STEP_DIST,
                'y1': lat - STEP_DIST,
                'x2': lng + STEP_DIST,
                'y2': lat - STEP_DIST,
                'x3': lng - STEP_DIST,
                'y3': lat + STEP_DIST,
                'x4': lng + STEP_DIST,
                'y4': lat + STEP_DIST,
            }
    return polygons


def create_dataset():
    # Создание полигонов
    polygons = create_polygons(LAT, LNG)

    # Наполнение полигонов погодными данными
    for polygon in polygons:
        polygons[polygon] |= weather_dataset(lat=polygon[0], lng=polygon[1])
        polygons[polygon] |= soil_dataset(lat=polygon[0], lng=polygon[1])
        print(polygon)


create_dataset()
