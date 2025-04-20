from django.urls import path
from . import views

app_name = 'game'

urlpatterns = [
    path('', views.game, name="ingame"),
    path('map', views.map, name="map"),
    path('event',views.event, name="event"),
    path('fight',views.fight, name="fight"),
    path('joker',views.joker, name="joker"),
    path('inventory', views.inventory),
    path('farm', views.farm),
    path('rest', views.rest),
    path('build', views.build),
    path('manager', views.manager, name="manager"),
    path('rip', views.rip, name="rip")
]