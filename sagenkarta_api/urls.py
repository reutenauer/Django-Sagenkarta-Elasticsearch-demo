from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^records/', views.getRecords, name='getRecords'),
]