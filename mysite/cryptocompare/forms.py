from django import forms
from .models import Portfolio





class Cryptoform(forms.Form):
    class Meta:
        model=Portfolio()
        fields=('coin_name', 'id')

