"""
URL configuration for busproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from .import views

urlpatterns = [
    path('', views.start),
    path('schedule_new/', views.take_schedule, name="schedule"),
    path('search/', views.search_bus, name="search_buses"),  # ✅ trailing slash + name
    path('book/', views.book_bus, name='book_bus'),
    path('schedule/', views.bus_schedule_search, name='bus_schedule_search'),
    path('api/update-location/', views.update_bus_location, name='update_location'),
    path('api/get-location/<str:bus_no>/', views.get_bus_location, name='get_location'),
    path('track/<int:bus_id>/', views.track_bus, name='track_bus'),
   
    # urls.py
    path('booking_history/', views.booking_history, name='booking_history'),
    path('book-bus-ajax/', views.book_bus_ajax, name='book_bus_ajax'),
]


