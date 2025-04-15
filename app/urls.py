# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from app import views

urlpatterns = [

    # The home page
    path('', views.dashboard, name='dashboard'),
    path('chart-data/', views.sensor_chart_data, name='sensor_chart_data'),
    # Matches any html file
    re_path(r'^.*\.html', views.pages, name='pages'),

]
