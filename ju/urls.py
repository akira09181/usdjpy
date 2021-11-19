from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name='index'),
    path('sma',views.sma,name='sma'),
    path('update',views.update,name='update'),
    path('breverse',views.breverse,name="breverse"),
]
