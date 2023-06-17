from django.db import models
from django.contrib.postgres.fields import ArrayField


# Create your models here.
class Polygons(models.Model):
    lat = models.FloatField(verbose_name="широта", null=True)
    lng = models.FloatField(verbose_name="долгота", null=True)
    x1 = models.FloatField(verbose_name="верхний левый угол", null=True)
    y1 = models.FloatField(verbose_name="верхний левый угол", null=True)
    x2 = models.FloatField(verbose_name="верхний правый угол", null=True)
    y2 = models.FloatField(verbose_name="верхний правый угол", null=True)
    x3 = models.FloatField(verbose_name="нижний правый угол", null=True)
    y3 = models.FloatField(verbose_name="нижний правый угол", null=True)
    x4 = models.FloatField(verbose_name="нижний левый угол", null=True)
    y4 = models.FloatField(verbose_name="нижний левый угол", null=True)
    elevation = models.IntegerField(verbose_name="высота", null=True)
    inclination = models.FloatField(verbose_name="максимальный угол наклона", null=True)
    # Погода
    temp = models.FloatField(verbose_name="температура", null=True)
    pressure = models.FloatField(verbose_name="давление", null=True)
    humidity = models.FloatField(verbose_name="влажность", null=True)
    wind_speed = models.FloatField(verbose_name="скорость ветра", null=True)
    wind_gust = models.FloatField(verbose_name="порыв ветра", null=True)
    clouds = models.FloatField(verbose_name="облачность", null=True)
    weather = ArrayField(models.CharField(max_length=200, verbose_name="тип погоды", null=True), blank=True, null=True)
    # Почва
    bdod = models.IntegerField(verbose_name="Объемная плотность", null=True)
    cec = models.IntegerField(verbose_name="Катионный обмен", null=True)
    cfvo = models.IntegerField(verbose_name="Крупные фрагменты", null=True)
    clay = models.IntegerField(verbose_name="Кол-во глины", null=True)
    nitrogen = models.IntegerField(verbose_name="Нитрогены", null=True)
    ocd = models.IntegerField(verbose_name="Плотность органического углерода", null=True)
    ocs = models.IntegerField(verbose_name="Запас органического углерода", null=True)
    phh2o = models.IntegerField(verbose_name="рН", null=True)
    sand = models.IntegerField(verbose_name="Кол-во песка", null=True)
    silt = models.IntegerField(verbose_name="Кол-во ила", null=True)
    soc = models.IntegerField(verbose_name="Концентрация органического углерода", null=True)
    # скоринг
    score = models.FloatField(verbose_name="скоринг", default=0.0, null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['lat', 'lng'], name='unique_migration_host_combination'
            )
        ]

