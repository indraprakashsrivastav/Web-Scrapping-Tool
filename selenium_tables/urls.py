from django.urls import path
from . import views

urlpatterns = [
    path('', views.url_input, name='home'), 
    path('tables/', views.fetch_tables, name='fetch_tables'),
    path('url/', views.url_input, name='url_input'),
    path('download/', views.download_table, name='download_table'),
]
