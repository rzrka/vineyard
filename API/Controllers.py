import pickle
from abc import ABC, abstractmethod
from dataclasses import dataclass
from entites import StateInt, CreatePolygons, PolygonAdminEnt, PolygonScinceEnt


class BaseControllerInt(ABC):
    '''
    Интерфейс контроллеров персонала
    '''

    @abstractmethod
    def create_polygons(self):
        '''
        Создание полигона
        :return:
        '''

    @abstractmethod
    def save_polygons(self):
        '''
        Сохранение полигонов
        :return:
        '''


class BaseController(BaseControllerInt):
    '''
    Базовый класс контроллера для создание полигонов
    '''

    def __init__(self):
        super().__init__()
        # стартовые координаты
        self._slat: float = 44.913408
        self._slng: float = 38.944393
        # размер карты
        self._size_x: int = 1000
        self._size_y: int = 1000
        # шаг в метрах
        self._meter: int = 125
        self._polygons = self.create_polygons()
        # Данные для сохранения полигонов
        self.path: str = ''
        self.filename: str = ''

    @property
    def polygons(self):
        return self._polygons

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

    def create_polygons(self) -> dict:
        '''
        Создание полигона
        :return:
        '''
        create_polygons = CreatePolygons(
            slat=self.slat,
            slng=self.slng,
            size_x=self.size_x,
            size_y=self.size_y,
            meter=self.meter,
        )
        polygons = create_polygons.create_polygons()
        polygons = create_polygons.set_elevation(polygons)
        polygons = create_polygons.set_inclination(polygons)
        return polygons

    def save_polygons(self):
        '''
        Сохранение полигонов
        :return:
        '''
        with open(self.path + self.filename, 'wb') as f:
            pickle.dump(self.polygons, f, protocol=pickle.HIGHEST_PROTOCOL)



class AdminController(BaseController):
    '''
    Выбор полигона для отображения на карте
    '''

    def __init__(self):
        super().__init__()
        # Данные для сохранения полигонов
        self.path = "../backend/polygons/datasets/"
        self.filename = "map.pickle"

    def get_polygons(self):
        '''
        Получение итоговых полигонов
        :return:
        '''
        for key, value in self.polygons.items():
            polygon = {key: value}
            polygon_ent = PolygonAdminEnt(polygon=polygon)
            # polygon_ent.set_weather()
            polygon_ent.set_soil()
            polygon_ent.scored_polygons()
        self.save_polygons()

class ScinceController(BaseController):
    '''
    Выбор полигонов для обучения
    '''

    def __init__(self):
        super().__init__()
        # Признак можно ли выращивать
        self.growing = True
        # Данные для сохранения полигонов
        self.path = "../ml/datasets/"
        self.filename = "vineyard7.pickle"

    def get_polygons(self):
        '''
        Создание полигонов для обучения
        :return:
        '''
        for key, value in self.polygons.items():
            polygon = {key: value}
            polygon_ent = PolygonScinceEnt(polygon=polygon, growing=self.growing)
            # polygon_ent.set_weather()
            polygon_ent.set_soil()
            polygon_ent.train_polygons()
        self.save_polygons()

ScinceController().get_polygons()