from django.urls import path
from . import views

urlpatterns = [
    path('', views.main_view, name='main'),
    path('map/<str:map_name>', views.map_view, name='map'),
    path('generator', views.generate_form_view, name='generator'),
    path('generate', views.generate_map, name='generate'),
    path('get_tooltip', views.get_tooltip, name='tooltip'),
    path('gallery/<str:gallery_type>', views.gallery_view, name='gallery'),
    path('users_gallery', views.users_gallery_view, name='users_gallery'),
    path('add_to_favourites', views.add_to_favourites, name="add_to_favourites"),
    path('login_view', views.login_view, name='login_view'),
    path('register_view', views.register_view, name='register_view'),
    path('logout_view', views.logout_view, name='logout_view'),

]
