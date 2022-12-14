# Generated by Django 4.1.3 on 2022-12-17 21:12

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Polygons',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lat', models.FloatField(null=True, verbose_name='широта')),
                ('lng', models.FloatField(null=True, verbose_name='долгота')),
                ('x1', models.FloatField(null=True, verbose_name='верхний левый угол')),
                ('y1', models.FloatField(null=True, verbose_name='верхний левый угол')),
                ('x2', models.FloatField(null=True, verbose_name='верхний правый угол')),
                ('y2', models.FloatField(null=True, verbose_name='верхний правый угол')),
                ('x3', models.FloatField(null=True, verbose_name='нижний правый угол')),
                ('y3', models.FloatField(null=True, verbose_name='нижний правый угол')),
                ('x4', models.FloatField(null=True, verbose_name='нижний левый угол')),
                ('y4', models.FloatField(null=True, verbose_name='нижний левый угол')),
                ('elevation', models.IntegerField(null=True, verbose_name='высота')),
                ('inclination', models.FloatField(null=True, verbose_name='максимальный угол наклона')),
                ('temp', models.FloatField(null=True, verbose_name='температура')),
                ('pressure', models.FloatField(null=True, verbose_name='давление')),
                ('humidity', models.FloatField(null=True, verbose_name='влажность')),
                ('wind_speed', models.FloatField(null=True, verbose_name='скорость ветра')),
                ('wind_gust', models.FloatField(null=True, verbose_name='порыв ветра')),
                ('clouds', models.FloatField(null=True, verbose_name='облачность')),
                ('weather', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=200, null=True, verbose_name='тип погоды'), blank=True, null=True, size=None)),
                ('bdod', models.IntegerField(null=True)),
                ('cec', models.IntegerField(null=True)),
                ('cfvo', models.IntegerField(null=True)),
                ('clay', models.IntegerField(null=True)),
                ('nitrogen', models.IntegerField(null=True)),
                ('ocd', models.IntegerField(null=True)),
                ('ocs', models.IntegerField(null=True)),
                ('phh2o', models.IntegerField(null=True)),
                ('sand', models.IntegerField(null=True)),
                ('silt', models.IntegerField(null=True)),
                ('soc', models.IntegerField(null=True)),
                ('score', models.FloatField(default=0.0)),
            ],
        ),
        migrations.AddConstraint(
            model_name='polygons',
            constraint=models.UniqueConstraint(fields=('lat', 'lng'), name='unique_migration_host_combination'),
        ),
    ]
