from django.urls import path
from leaf_detection import views

urlpatterns = [
    path('leaf_classifier_home', views.leaf_classifier_home, name="leaf_classifier_home"),
    path('leaf_result', views.leaf_result, name="leaf_result")
]
