from rest_framework import permissions
from rest_framework.viewsets import ModelViewSet, ViewSet
from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer
from django.conf import settings
from rest_framework.response import Response
from .models import Polygons
from .serializers import PolygonsSerializer


class PolygonsModelViewSet(ViewSet):
    renderer_classes = [JSONRenderer, BrowsableAPIRenderer]
    permission_classes = [permissions.AllowAny]

    def list(self, request):
        # получение всех полигонов
        polygons = Polygons.objects.all()
        # сериализации плигонов
        serializer = PolygonsSerializer(polygons, many=True)
        return Response(serializer.data)

