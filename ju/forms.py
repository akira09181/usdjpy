from django import forms
from .models import Bre, Sma

class Sma(forms.ModelForm):
    class Meta:
        model = Sma
        fields = ('short','long','val','sjpy')
class BreForm(forms.ModelForm):
    class Meta:
        model= Bre
        fields = ('moveline','val','sjpy')