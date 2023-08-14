from django.urls import path
from . import views

urlpatterns = [
    path('', views.main_view, name='main'),
    path('map/<str:map_name>', views.map_view, name='map'),
    path('generator', views.generate_form_view, name='generator'),
    path('generate', views.generate_map, name='generate'),

]
