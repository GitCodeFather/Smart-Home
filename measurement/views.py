from rest_framework.generics import ListAPIView, RetrieveAPIView
from .models import Sensor
from .serializers import SensorSerializer, SensorDetailSerializer


class SensorListView(ListAPIView):
    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer


class SensorDetailView(RetrieveAPIView):
    queryset = Sensor.objects.all()
    serializer_class = SensorDetailSerializer

