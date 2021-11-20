from django.db import models

# Create your models here.
class PastValue (models.Model):
    date = models.DateField(primary_key=True)
    start = models.FloatField(max_length=100)
    high = models.FloatField(max_length=100)
    low = models.FloatField(max_length=100)
    end = models.FloatField(max_length=100)
    
class Sma(models.Model):
    short = models.IntegerField(default=5,verbose_name="短い移動平均線")
    long = models.IntegerField(default=14,verbose_name="長い移動平均線")
    val = models.IntegerField(default=30,verbose_name="取引量（％）")
    sjpy = models.IntegerField(default=100,verbose_name="初期投資額（JPY）")

class Bre(models.Model):
    moveline = models.IntegerField(default=20,verbose_name="移動平均線（日）")
    val = models.IntegerField(default=30,verbose_name="取引量（％）")
    sjpy = models.IntegerField(default=100000,verbose_name="初期投資額（円）")