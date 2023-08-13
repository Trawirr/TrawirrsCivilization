from django.urls import path
from . import views

urlpatterns = [
    path('', views.main_view, name='main'),
    path('map/<str:map_name>', views.map_view, name='map'),
]
