from django.db import models

# Create your models here.

class Shares(models.Model):
    name = models.CharField(max_length=255)


class Transactions(models.Model):
    BUY_SELL = (('BUY', 'Buy'),('SELL', 'Sell'))
    share = models.ForeignKey(Shares, on_delete=models.CASCADE)
    date = models.DateField()
    buy_sell = models.CharField(max_length=4, choices=BUY_SELL)
    number = models.IntegerField()
    cost = models.DecimalField(max_digits=12, decimal_places=4)


class Price_Changes(models.Model):
    share = models.ForeignKey(Shares, on_delete=models.CASCADE)
    date = models.DateField()
    price = models.DecimalField(max_digits=12, decimal_places=4)

