from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name='index'),
    path('sma',views.sma,name='sma'),
    path('update',views.update,name='update'),
    path('breverse',views.breverse,name="breverse"),
    path('bbr',views.bbr,name='bbr'),
    path('rsi',views.rsi,name='rsi'),
]
