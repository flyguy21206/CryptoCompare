from django.contrib.auth import get_user_model
from django.db import models
from django.contrib.auth.models import User
import uuid

class Portfolio(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image_url = models.URLField( max_length=50, blank = True, null = True)
    coin_name = models.CharField( max_length=50, blank = True, null = True)
    ticker = models.CharField(max_length=50, blank = True, null = True)
    current_price = models.DecimalField(default=0, max_digits=40, decimal_places=20)
    volume = models.IntegerField(default=0)
    high_price = models.DecimalField(default=0, max_digits=40, decimal_places=20)
    low_price = models.DecimalField(default=0, max_digits=40, decimal_places=20)

    def __str__(self):
         return self.coin_name




