from rest_framework.serializers import ModelSerializer
from .models import Polygons


class PolygonsSerializer(ModelSerializer):

    class Meta:
        model = Polygons
        fields = '__all__'