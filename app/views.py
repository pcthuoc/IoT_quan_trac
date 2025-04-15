# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.http import HttpResponse
from django import template
from sensors.models import Sensors,SensorData
from django.utils.timezone import now, timedelta
from django.http import JsonResponse
from django.conf import settings
import requests

@login_required(login_url="/login/")
def dashboard(request):
    sensors = Sensors.objects.all()

    context = {
        'segment': 'dashboard',
        'sensors': sensors,
    }

    html_template = loader.get_template('dashboard.html')
    return HttpResponse(html_template.render(context, request))
def sensor_chart_data(request):
    time_range = request.GET.get('range', '24h')

    time_map = {
        '1h': timedelta(hours=1),
        '3h': timedelta(hours=3),
        '6h': timedelta(hours=6),
        '12h': timedelta(hours=12),
        '24h': timedelta(hours=24),
        '3d': timedelta(days=3),
        '7d': timedelta(days=7),
    }

    duration = time_map.get(time_range, timedelta(hours=24))
    time_threshold = now() - duration

    data = {}
    sensors = Sensors.objects.all()

    for sensor in sensors:
        logs = SensorData.objects.filter(sensor=sensor, timestamp__gte=time_threshold).order_by('timestamp')
        data[sensor.sensor_name] = [
            {
                'x': log.timestamp.isoformat(),  # ApexCharts cần ISO format
                'y': log.value
            } for log in logs
        ]

    return JsonResponse(data)

@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]
        context['segment'] = load_template

        html_template = loader.get_template(load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:

        html_template = loader.get_template('page-500.html')
        return HttpResponse(html_template.render(context, request))
