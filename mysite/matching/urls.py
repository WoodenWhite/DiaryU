from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('emotion/', views.emotion, name='emotion'),
    path('depair/', views.depair, name='depair'),
    path('depair_action/', views.depair_action, name='depair_action')
]
