from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('check_face/', views.check_face, name='check_face')
]