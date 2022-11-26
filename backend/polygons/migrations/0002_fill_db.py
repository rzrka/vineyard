from django.db import migrations
from django.conf import settings
import pickle
import os


def forwards_func(apps, schema_editor):
    polygons_model = apps.get_model("polygons", "Polygons")  # Load model for make changes
    pk = 1
    with open(os.path.join(settings.BASE_DIR, 'polygons/datasets/dataset.pickle'), 'rb') as f:
        data = pickle.load(f)
        for key, values in data.items():
            polygons_model.objects.create(
                pk=pk,
                lat=key[0],
                lng=key[1],
                x1=values['x1'],
                y1=values['y1'],
                x2=values['x2'],
                y2=values['y2'],
                x3=values['x3'],
                y3=values['y3'],
                x4=values['x4'],
                y4=values['y4'],
                temp=values['temp'],
                pressure=values['pressure'],
                humidity=values['humidity'],
                wind_speed=values['wind_speed'],
                wind_gust=values['wind_gust'],
                clouds=values['clouds'],
                weather=list(values['weather']),
                bdod=values['bdod']['0-5cm'],
                cec=values['cec']['0-5cm'],
                cfvo=values['cfvo']['0-5cm'],
                clay=values['clay']['0-5cm'],
                nitrogen=values['nitrogen']['0-5cm'],
                ocd=values['ocd']['0-5cm'],
                ocs=values['ocs']['0-30cm'],
                phh2o=values['phh2o']['0-5cm'],
                sand=values['sand']['0-5cm'],
                silt=values['silt']['0-5cm'],
                soc=values['soc']['0-5cm'],
                score=100 if values['bdod']['0-5cm'] else 0
            )
            pk += 1
    del polygons_model  # Delete link for category


def reverse_func(apps, schema_editor):
    polygons_model = apps.get_model("polygons", "Polygons")  # Load model for make changes

    # Delete all objects
    polygons_model.objects.all().delete()


class Migration(migrations.Migration):
    dependencies = [("polygons", "0001_initial")]

    operations = [migrations.RunPython(forwards_func, reverse_func)]
