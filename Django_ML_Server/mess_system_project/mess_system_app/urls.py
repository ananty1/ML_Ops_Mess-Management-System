from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name='home'),
    path('popularDish',views.popular_dishes,name='popular_dishes'),
    path('predict', views.predict_view, name='predict'),
    path('get-latest-footprint-graph', views.getGraph, name='getGraph'),
]

