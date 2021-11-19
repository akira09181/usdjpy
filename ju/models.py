from django.db import models

# Create your models here.
class PastValue (models.Model):
    date = models.DateField(primary_key=True)
    start = models.FloatField(max_length=100)
    high = models.FloatField(max_length=100)
    low = models.FloatField(max_length=100)
    end = models.FloatField(max_length=100)
    
class Sma(models.Model):
    short = models.IntegerField(default=5)
    long = models.IntegerField(default=14)
    val = models.IntegerField(default=30)
    sjpy = models.IntegerField(default=100)