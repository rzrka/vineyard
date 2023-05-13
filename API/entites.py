from abc import abstractmethod, ABC
import abc
import json
import datetime
import pickle
import urllib
import os
import urllib3
from geopy.distance import Distance
from geopy.units import degrees, nautical
import requests
from dataclasses import dataclass
import math
import datetime
import time
from enum import Enum
from statistics import mean
import pandas as pd
import numpy as np


os.environ['OPENWEATHER_API'] = '814d14d83f45f882b976078494e7a81a'
os.environ[
    'ELEVATION_API'] = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjcmVkZW50aWFsX2lkIjoiY3JlZGVudGlhbHxabmVtOU40dEVkV2xlWGhFV2txbHBJcXFFS0pnIiwiYXBwbGljYXRpb25faWQiOiJhcHBsaWNhdGlvbnxOS1FLOUFCSUVrekVENVVaMHFOZVJUbGRxUU0iLCJvcmdhbml6YXRpb25faWQiOiJkZXZlbG9wZXJ8TGJiZ2J2d2hPMmd5b3Z1RERRMjdZSFduZEpiQSIsImlhdCI6MTY3MTQ1MjY0OH0.BT_o_E-8oXbn7T0inrRGvKScXtCpWq8hhAvtVrlInJU"


class CreatePolygonsInt(ABC):
    '''
    Интерфейс создание набора полигонов
    '''

    @abstractmethod
    def create_polygons(self) -> {(tuple, tuple): dict}:
        '''
        создание списка полигонов с координатами
        '''

    @abstractmethod
    def set_inclination(self, polygons) -> {(tuple, tuple): dict}:
        '''
        Расчет и присвоение угла наклона
        '''

    @abstractmethod
    def set_elevation(self, polygons: {(tuple, tuple): dict}) -> dict:
        '''
        присвоение высоты
        '''


class CreatePolygons(CreatePolygonsInt):
    '''
        Интерфейс создание набора полигонов
        '''

    def __init__(self, slat: float, slng: float, size_x: int, size_y: int, meter: int):
        super().__init__()
        # стартовые координаты
        self._slat: float = slat
        self._slng: float = slng
        # размер карты
        self._size_x: int = size_x
        self._size_y: int = size_y
        # шаг в метрах
        self._meter: int = 0
        # шаг в градусах
        self._degress: float = 0
        self.meter = meter
        self.degress = meter
    @property
    def slat(self):
        return self._slat

    @property
    def slng(self):
        return self._slng

    @property
    def size_x(self):
        return self._size_x

    @property
    def size_y(self):
        return self._size_y

    @property
    def meter(self):
        return self._meter

    @meter.setter
    def meter(self, meter: int):
        self._meter = meter

    @property
    def degress(self):
        '''
        получение шага
        :return:
        '''
        return self._degress

    @degress.setter
    def degress(self, meter: int) -> None:
        '''
        Установка шага
        :param meter:
        :return:
        '''
        rough_distance = degrees(arcminutes=nautical(meters=meter))
        self._degress = round(rough_distance, 6)

    def create_polygons(self) -> {(tuple, tuple): dict}:
        '''
        создание списка полигонов с координатами
        :param lat: float, широта
        :param lng: float, долгота
        :return:
        '''

        polygons = {}
        # конечные координаты
        stop_lat = self.slat - (self.size_y / self.meter) * self.degress
        stop_lng = self.slng + (self.size_x / self.meter) * self.degress
        # расстояние между центральными точками полигонов
        step = int(self.degress * 1000000 * 2)

        # перевод координат в int
        start_lat = int(self.slat * 1000000)
        start_lng = int(self.slng * 1000000)
        stop_lat = int(stop_lat * 1000000)
        stop_lng = int(stop_lng * 1000000)

        for lat in range(start_lat, stop_lat, -step):
            # перевод координат в float для записи
            lat /= 1000000
            for lng in range(start_lng, stop_lng, step):
                # перевод координат в float для записи
                lng /= 1000000
                polygons[(lat, lng)] = {
                    # запись координат по углам квадрата полигона
                    'x1': round(lng - self.degress, 6),
                    'y1': round(lat - self.degress, 6),
                    'x2': round(lng + self.degress, 6),
                    'y2': round(lat - self.degress, 6),
                    'x3': round(lng - self.degress, 6),
                    'y3': round(lat + self.degress, 6),
                    'x4': round(lng + self.degress, 6),
                    'y4': round(lat + self.degress, 6),
                }
        return polygons

    def set_elevation(self, polygons: {(tuple, tuple): dict}) -> dict:
        '''
        присвоение высоты
        '''
        for polygon in polygons:
            lat = polygon[0]
            lng = polygon[1]
            url = f"https://api.airmap.com/elevation/v1/ele/?points={lat},{lng}"
            request = requests.get(url, headers={'X-API-Key': os.environ['ELEVATION_API']})
            response = request.json()
            elevation = response['data'][0]
            polygons[polygon] |= {'elevation': elevation}
        return polygons

    def set_inclination(self, polygons: {(tuple, tuple): dict}) -> {(tuple, tuple): dict}:
        '''
        Расчет и присвоение угла наклона
        '''

        for polygon in polygons:
            polygon_degress = 0
            # Список соседних полигонов
            neighbor_poligons = [
                (polygon[0], round(polygon[1] + (self.degress * 2), 6)),
                (polygon[0], round(polygon[1] - (self.degress * 2), 6)),
                (round(polygon[0] + (self.degress * 2), 6), polygon[1]),
                (round(polygon[0] - (self.degress * 2), 6), polygon[1]),

            ]
            for neighbor_poligon in neighbor_poligons:
                try:
                    cur_neighbor = polygons[neighbor_poligon]
                    height = abs(polygons[polygon]['elevation'] - cur_neighbor['elevation'])
                except Exception as e:
                    print(e)
                    continue
                b = self.meter
                result = math.degrees(math.atan(height / b))
                if result > polygon_degress:
                    polygon_degress = result
            polygons[polygon]['inclination'] = polygon_degress
        return polygons


class StateInt(metaclass=abc.ABCMeta):
    '''
    Базовый класс состояния
    '''

    context: dict = None

    @abstractmethod
    def set_weather(self):
        """
        Получение погодных данных
        """
        pass

    @abstractmethod
    def set_soil(self):
        """
        Получение почвеных данных
        """
        pass

    @abstractmethod
    def scored_polygons(self):
        '''
        Наполнение полигонов коэффициентом похожести
        '''
        pass

    @abstractmethod
    def train_polygons(self):
        '''
        Наполнение полигонов данными для использование их в обучение модели
        '''
        pass


class PolygonsBase(StateInt):
    '''
    Базовый класс для работы с полигоном
    '''

    def update_context(self, polygon):
        '''
        обновление данных у полигона
        :return:
        '''
        self.context.polygon[[i for i in self.context.polygon][0]] |= polygon


class PolygonNewState(PolygonsBase):
    '''
    Состояние для наполнение полигонов
    '''

    def set_weather(self):
        """
        Получение погодных данных
        :param lat: float, широта
        :param lng: float, долгота
        :return: dict
        """
        lat = self.context.polygon[0]
        lng = self.context.polygon[1]
        # Временной промежуток за которой берутся данные
        start_date = int(time.mktime(datetime.datetime.strptime('2022-07-01', "%Y-%m-%d").timetuple()))
        end_date = int(time.mktime(datetime.datetime.strptime('2022-07-08', "%Y-%m-%d").timetuple()))
        url = f"https://history.openweathermap.org/data/2.5/history/city?lat={lat}&lon={lng}&type=hour&start={start_date}&end={end_date}&appid={os.environ['OPENWEATHER_API']}"
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

        self.update_context(dataset)

    def set_soil(self):
        """
        Получение почвеных данных
        """
        lat = list(self.context.polygon.keys())[0][0]
        lng = list(self.context.polygon.keys())[0][1]
        query_params = {'lat': lat, "lon": lng}

        REST_URL = "https://rest.isric.org"
        prop_query_url = f"{REST_URL}/soilgrids/v2.0/properties/query"

        response = requests.get(prop_query_url, params={**query_params, })
        data = response.json()
        dataset = {}
        for layer in data['properties']['layers']:
            soil_data = {layer['name']: {}}
            value = layer['depths'][0]
            soil_data[layer['name']] = value['values'].get('mean')
            dataset |= soil_data

        self.update_context(dataset)

    def scored_polygons(self):
        '''
        Наполнение полигонов коэффициентом похожести
        '''
        raise Exception

    def train_polygons(self):
        '''
        Наполнение полигонов данными для использование их в обучение модели
        '''
        raise Exception

    def close(self):
        '''
        Сохранение полигонов
        :return:
        '''
        raise Exception


class PolygonScoredState(PolygonsBase):
    '''
    Состояние оценки полигонов
    '''

    def __init__(self):
        self._model_path = '../ml/models/model.pkl'
        self._model = self.load_model()
        # Список колонок которые не участвуют в модели
        self._params_for_model = ['x1', 'y1', 'x2', 'y2', 'x3', 'y3', 'x4', 'y4', 'inclination', 'weather', 'elevation',
                                  'wind_gust']
        # Список вариаций погоды
        self._weather_types = {
            'broken clouds',
            'clear sky',
            'few clouds',
            'fog',
            'haze',
            'heavy intensity rain',
            'light rain',
            'light snow',
            'mist',
            'moderate rain',
            'moderate rainmist',
            'overcast clouds',
            'scattered clouds',
            'snow',
            'thunderstorm',
            'very heavy rain'
        }

    def set_weather(self):
        """
        Получение погодных данных
        """
        raise Exception

    def set_soil(self):
        """
        Получение почвеных данных
        """
        raise Exception

    def train_polygons(self):
        '''
        Наполнение полигонов данными для использование их в обучение модели
        '''
        raise Exception

    @property
    def weather_types(self) -> set:
        return self._weather_types

    @property
    def params_for_model(self) -> list:
        return self._params_for_model

    @property
    def model_path(self) -> str:
        '''
        Путь где хранится ML модель
        :return:
        '''
        return self._model_path

    @property
    def model(self) -> pickle:
        '''
        получить ML модель
        :return:
        '''
        return self._model

    @model.setter
    def model(self, model: pickle) -> pickle:
        '''
        Задать ML модель
        :param model:
        :return:
        '''
        self._model = model

    def load_model(self) -> None:
        '''
        Загрузка модели
        :return:
        '''
        with open(self.model_path, "rb") as f:
            self.model = pickle.load(f)

    def custom_dummies_weather(self, df: pd.DataFrame) -> pd.DataFrame:
        '''
        Преобразование списка вариаций погоды в нормальный вид для модели
        :param df:
        :return:
        '''
        df['weather'] = df['weather'].apply(lambda x: tuple(x))
        arr = {}
        for weather_type in self.weather_types:
            for weather_el in df['weather']:
                if weather_type in weather_el:
                    if arr.get(weather_type):
                        arr.get(weather_type).append(1)
                    else:
                        arr[weather_type] = [1]
                else:
                    if arr.get(weather_type):
                        arr.get(weather_type).append(0)
                    else:
                        arr[weather_type] = [0]

        arr = pd.DataFrame.from_dict(arr)
        return arr

    def score_feather_inclination(self, df: pd.DataFrame) -> None:
        '''
        Выставление оценки в зависимости от наклона полигона
        :param df:
        :return:
        '''
        df.loc[df.inclination > 45.0, 'score'] = 0

    def scored_polygons(self) -> None:
        '''
        Оценивание полигонов
        :param polygons:
        :return:
        '''
        # подготовка данных для получение
        df = pd.DataFrame.from_dict(self.context.polygon.values())
        lat_lng = pd.DataFrame.from_dict(self.context.polygon.keys()).rename(columns={0: "lat", 1: "lng"})
        db_attr = df[self.params_for_model]
        df = pd.concat([df, self.custom_dummies_weather(df)], axis=1)
        df = df.drop(self.params_for_model, axis=1)
        df = df.dropna().reset_index(drop=True)
        # получение скоринга
        predicted = self.model.predict_proba(df)

        # объеденение данных которые не участвывали в скоринга со скорингом
        series_score = pd.Series(predicted[:, 1], name='score').apply(lambda x: x * 100)
        df = pd.concat([df, series_score, lat_lng, db_attr], axis=1)
        df = df.replace({np.nan: None})

        # изменение оценок по фичам
        self.score_feather_inclination(df)

        # сохранение полигонов
        self.update_context(df['score'].to_dict())


class PolygonTrainState(PolygonsBase):

    def __init__(self):
        ...


    def set_weather(self):
        """
        Получение погодных данных
        """
        raise Exception

    def set_soil(self):
        """
        Получение почвеных данных
        """
        raise Exception

    def scored_polygons(self):
        '''
        Наполнение полигонов коэффициентом похожести
        '''
        raise Exception

    def train_polygons(self):
        '''
        Наполнение полигонов данными для использование их в обучение модели
        '''
        self.context.polygon[[_ for _ in self.context.polygon][0]]['growing'] = self.context.growing


class PolygonStates(Enum):
    '''
    Возможные состояния полигонов по их созданию
    '''

    new = PolygonNewState
    train = PolygonTrainState
    scored = PolygonScoredState


class PolygonAdminEnt:
    '''
    Сущность "Полигона"
    '''
    _state: StateInt = None

    def __init__(
            self,
            polygon: dict,
            state: str = 'new',
    ):
        self.polygon = polygon
        self.transition_to(getattr(PolygonStates, state).value())


    def set_weather(self):
        """
        Получение погодных данных
        """
        self._state.set_weather()

    def set_soil(self):
        """
        Получение почвеных данных
        """
        self._state.set_soil()
        self.transition_to(PolygonStates.scored.value())

    def scored_polygons(self):
        '''
        Наполнение полигонов коэффициентом похожести
        '''
        self._state.scored_polygons()

    def train_polygons(self):
        '''
        Наполнение полигонов данными для использование их в обучение модели
        '''
        self._state.train_polygons()

    def transition_to(self, state: StateInt):
        '''
        Перейти на новое состояние
        :param state:
        :return:
        '''
        self._state = state
        self._state.context = self


class PolygonScinceEnt:
    '''
    Сущность "Полигона"
    '''
    _state: StateInt = None

    def __init__(
            self,
            polygon: dict,
            growing: bool,
            state: str = 'new',
    ):
        self.polygon = polygon
        self.growing = growing
        self.transition_to(getattr(PolygonStates, state).value())


    def set_weather(self):
        """
        Получение погодных данных
        """
        self._state.set_weather()

    def set_soil(self):
        """
        Получение почвеных данных
        """
        self._state.set_soil()
        self.transition_to(PolygonStates.train.value())

    def train_polygons(self):
        '''
        Наполнение полигонов данными для использование их в обучение модели
        '''
        self._state.train_polygons()

    def transition_to(self, state: StateInt):
        '''
        Перейти на новое состояние
        :param state:
        :return:
        '''
        self._state = state
        self._state.context = self
