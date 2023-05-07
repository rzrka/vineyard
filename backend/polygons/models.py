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
    temp = models.FloatField(verbose_name="температура", null=True)
    pressure = models.FloatField(verbose_name="давление", null=True)
    humidity = models.FloatField(verbose_name="влажность", null=True)
    wind_speed = models.FloatField(verbose_name="скорость ветра", null=True)
    wind_gust = models.FloatField(verbose_name="порыв ветра", null=True)
    clouds = models.FloatField(verbose_name="облачность", null=True)
    weather = ArrayField(models.CharField(max_length=200, verbose_name="тип погоды", null=True), blank=True, null=True)
    bdod = models.IntegerField(null=True)
    cec = models.IntegerField(null=True)
    cfvo = models.IntegerField(null=True)
    clay = models.IntegerField(null=True)
    nitrogen = models.IntegerField(null=True)
    ocd = models.IntegerField(null=True)
    ocs = models.IntegerField(null=True)
    phh2o = models.IntegerField(null=True)
    sand = models.IntegerField(null=True)
    silt = models.IntegerField(null=True)
    soc = models.IntegerField(null=True)
    score = models.FloatField(default=0.0, null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['lat', 'lng'], name='unique_migration_host_combination'
            )
        ]