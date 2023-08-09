from django.urls import path

from . import views

urlpatterns = [
    path('', views.home_page, name='home'),
    path('predictions/', views.predictions, name='predictions'),
    path('monitoring/', views.monitoring, name='monitoring'),
    path('historique/', views.historique, name='historique'),
]
