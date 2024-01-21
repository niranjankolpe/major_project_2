from django.urls import path, include
from detector_app import views

urlpatterns = [
    path('',    views.index, name="index"),
    path('home', views.home, name="home"),
    path('detector', views.detector, name="detector"),
    path('start_detection', views.start_detection, name="start_detection")
]
