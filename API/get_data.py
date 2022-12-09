import json
import datetime
import pickle
import urllib

import urllib3
from geopy.distance import Distance
from geopy.units import degrees, nautical
import requests

import datetime
import time

from statistics import mean

# LAT, LNG = 44.914533, 38.945518  # стартовые координаты
LAT, LNG = 44.652361, 7.939853
def get_degress(meter):
    rough_distance = degrees(arcminutes=nautical(meters=meter))
    return {'degress': round(rough_distance, 6), 'meters': meter}

STEP_DIST = get_degress(125)  # 125м,  шаг в градусах


MAX_SIZE_X, MAX_SIZE_Y = (6000, 8000)  # размер карты,в метрах
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

    # Температура
    temp = [x['main']['temp'] - 273.15 for x in data]
    if not None in temp:
        dataset['temp'] = round(mean([x for x in temp]), 2)
    else:
        dataset['temp'] = None

    # Давление
    pressure = [x['main'].get('pressure') for x in data]
    if not None in pressure:
        dataset['pressure'] = round(mean([x for x in pressure]), 2)
    else:
        dataset['pressure'] = None

    # Влажность
    humidity = [x['main'].get('humidity') for x in data]
    if not None in humidity:
        dataset['humidity'] = round(mean([x for x in humidity]), 2)
    else:
        dataset['humidity'] = None

    # Скорость ветра
    wind_speed = [x['wind'].get('speed') for x in data]
    if not None in wind_speed:
        dataset['wind_speed'] = round(mean([x for x in wind_speed]), 2)
    else:
        dataset['wind_speed'] = None

    # порыв ветра
    wind_gust = [x['wind'].get('gust') for x in data]
    if not None in wind_gust:
        dataset['wind_gust'] = round(mean([x for x in wind_gust]), 2)
    else:
        dataset['wind_gust'] = None

    # облачность, %
    clouds = [x['clouds'].get('all') for x in data]
    if not None in clouds:
        dataset['clouds'] = round(mean([x for x in clouds]), 2)
    else:
        dataset['clouds'] = None

    # Тип погоды
    weather = [i.get('weather') for i in data]
    if not None in weather:
        dataset['weather'] = {''.join(tuple(l.get('description') for l in j)) for j in
                              weather}
    else:
        dataset['clouds'] = None

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
        value = layer['depths'][0]
        soil_data[layer['name']][value['label']] = value['values'].get('mean')
        data_set |= soil_data

    return data_set


def create_polygons(slat, slng):
    '''
    step - расстояние между центральными точками двух полигонов,
    :param slat:
    :param slng:
    :return:
    '''
    polygons = {}
    stop_lat = slat - (MAX_SIZE_Y / STEP_DIST['meters']) * STEP_DIST['degress']
    stop_lng = slng + (MAX_SIZE_X / STEP_DIST['meters']) * STEP_DIST['degress']
    step = int(STEP_DIST['degress'] * 1000000 * 2)

    start_lat = int(slat * 1000000)
    start_lng = int(slng * 1000000)
    stop_lat = int(stop_lat * 1000000)
    stop_lng = int(stop_lng * 1000000)

    for lat in range(start_lat, stop_lat, -step):
        lat /= 1000000
        for lng in range(start_lng, stop_lng, step):
            lng /= 1000000
            polygons[(lat, lng)] = {
                'x1': round(lng - STEP_DIST['degress'], 6),
                'y1': round(lat - STEP_DIST['degress'], 6),
                'x2': round(lng + STEP_DIST['degress'], 6),
                'y2': round(lat - STEP_DIST['degress'], 6),
                'x3': round(lng - STEP_DIST['degress'], 6),
                'y3': round(lat + STEP_DIST['degress'], 6),
                'x4': round(lng + STEP_DIST['degress'], 6),
                'y4': round(lat + STEP_DIST['degress'], 6),
            }
    return polygons

def save_dataset(data):
    with open('../backend/polygons/datasets/vineyard6.pickle', 'wb') as f:
        pickle.dump(data, f, protocol=pickle.HIGHEST_PROTOCOL)

def get_elevation(lat, lng) -> dict:
    # получение высоты
    query = ('https://api.open-elevation.com/api/v1/lookup'
             f'?locations={lat},{lng}')
    elevation = requests.get(query).json()['results'][0]['elevation']
    return {'elevation': elevation}

def create_dataset():
    # Создание полигонов
    polygons_set = create_polygons(LAT, LNG)
    # Наполнение полигонов погодными данными
    polygons = iter(polygons_set)
    polygon = next(polygons)
    while True:
        try:
            polygons_set[polygon] |= get_elevation(lat=polygon[0], lng=polygon[1])
            polygons_set[polygon] |= weather_dataset(lat=polygon[0], lng=polygon[1])
            polygons_set[polygon] |= soil_dataset(lat=polygon[0], lng=polygon[1])
            print(polygons_set[polygon])
            polygon = next(polygons)
        except StopIteration:
            break
        except Exception as e:
            print(e)
            time.sleep(1)
    save_dataset(polygons_set)


create_dataset()
