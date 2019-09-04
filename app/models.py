from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.db import models
from django.contrib import auth


class User(auth.models.User, auth.models.PermissionsMixin):

    def __str__(self):
        return self.username

class Portfolio(models.Model):
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE)

class Stock(models.Model):
    roc = models.CharField(max_length=15)
    symbol	=   models.CharField(max_length=15)
    day_open = models.IntegerField()	
    day_high = models.IntegerField()
    day_low	= models.IntegerField()
    price = models.IntegerField()	
    volume = models.IntegerField()		
    previous_close = models.IntegerField()	
    change = models.IntegerField()
    change_percent = models.CharField(max_length=15)
    portfolio = models.ForeignKey('Portfolio', related_name='portfolio', on_delete=models.CASCADE)
    invested_date = models.DateTimeField()

    def get_amount(self):
        return self.volume*self.price