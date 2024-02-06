from django.urls import path
from leaf_detection import views

urlpatterns = [
    path('leaf_detector', views.leaf_detector, name="leaf_detector"),
    path('leaf_result', views.leaf_result, name="leaf_result")
]
