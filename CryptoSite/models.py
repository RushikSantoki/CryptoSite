from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here

class Crypto(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return str(self.id)


class Status(models.Model):
    currency_rank = models.CharField(max_length=10, default=0)
    currency_name = models.CharField(max_length=100, default='0')
    symbol = models.CharField(max_length=10, default='N/A')
    currency_price = models.CharField(max_length=100, default='0')
    percent_change_24h = models.CharField(max_length=100, default='0')
    percent_change_7d = models.CharField(max_length=100, default='0')
    percent_change_1h = models.CharField(max_length=100, default='0')
    market_cap = models.CharField(max_length=100, default='0')
    percent_change_30d = models.CharField(max_length=100, default='0')
    percent_change_60d = models.CharField(max_length=100, default='0')
    percent_change_90d = models.CharField(max_length=100, default='0')

    def __str__(self):
        return str(self.currency_name)


class Icons(models.Model):
    name = models.CharField(max_length=100, default='No currency', null=True)
    icon = models.URLField(null=True, default='www.google.com')

    def __str__(self):
        return self.name


class currencyUser(models.Model):
    unique = models.CharField(max_length=100, default='N/A', null=True)
    amount = models.CharField(max_length=100, default='0', null=True)
    crypto_name = models.CharField(max_length=100, default='N/A', null=True)
    bought_at = models.CharField(max_length=100, default='0', null=True)
    total_price = models.CharField(max_length=100, default='0', null=True)

    def __str__(self):
        return self.crypto_name + ", " + self.total_price
