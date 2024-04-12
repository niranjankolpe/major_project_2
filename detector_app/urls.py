from django.urls import path, include
from detector_app import views

urlpatterns = [
    path('',    views.index, name="index"),
    path('home', views.home, name="home"),
    path('detector', views.detector, name="detector"),
    path('homemade_remedies', views.homemade_remedies, name="homemade_remedies"),
    path('start_detection', views.start_detection, name="start_detection"),
    path('image_classify', views.image_classify, name="image_classify"),
]
