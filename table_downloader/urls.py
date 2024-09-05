from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponseRedirect

urlpatterns = [
    path('', lambda request: HttpResponseRedirect('selenium/')),  # Redirect root to /selenium/
    path('selenium/', include('selenium_tables.urls')),
]
