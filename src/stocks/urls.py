from django.urls import path

from . import views

urlpatterns = [
    path('', views.stocks, name='stocks'),
    path('stock', views.stock, name='stock'),
    path('analyze', views.analyze, name='analyze'),
]
