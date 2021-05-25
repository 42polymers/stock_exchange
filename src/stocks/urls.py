from django.urls import path

from . import views

urlpatterns = [
    path('', views.stocks, name='stocks'),
    path('stock', views.stock, name='stock'),
    path('double/<str:ticker1>_<str:ticker2>', views.double, name='double'),
    path('diff/<str:ticker1>_<str:ticker2>', views.diff, name='diff'),
]
