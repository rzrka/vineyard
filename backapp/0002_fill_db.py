from django.db import migrations
from django.conf import settings
import pickle
import os
import pandas as pd

def forwards_func(apps, schema_editor):
    polygons_model = apps.get_model("polygons", "Polygons")  # Load model for make changes
    pk = 1
    with open(os.path.join(settings.BASE_DIR, 'polygons/datasets/map1.pickle'), 'rb') as f:
        data = pickle.load(f)
        for _, row in data.iterrows():
            polygons_model.objects.create(
                pk=pk,
                lat=row['lat'],
                lng=row['lng'],
                x1=row['x1'],
                y1=row['y1'],
                x2=row['x2'],
                y2=row['y2'],
                x3=row['x3'],
                y3=row['y3'],
                x4=row['x4'],
                y4=row['y4'],
                # elevation=row['elevation'],
                # inclination=row['inclination'],
                temp=row['temp'],
                pressure=row['pressure'],
                humidity=row['humidity'],
                wind_speed=row['wind_speed'],
                wind_gust=row['wind_gust'],
                clouds=row['clouds'],
                weather=list(row['weather']),
                bdod=row['bdod'],
                cec=row['cec'],
                cfvo=row['cfvo'],
                clay=row['clay'],
                nitrogen=row['nitrogen'],
                ocd=row['ocd'],
                ocs=row['ocs'],
                phh2o=row['phh2o'],
                sand=row['sand'],
                silt=row['silt'],
                soc=row['soc'],
                score=row['score'],
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
