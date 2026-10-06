from django.urls import path
from .views import SensorListView, SensorDetailView


urlpatterns = [
    path('sensors/', SensorListView.as_view()),
    path('sensors/<int:pk>/', SensorDetailView.as_view())
]
