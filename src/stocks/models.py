from django.db import models


class Stock(models.Model):

    ticker = models.CharField(max_length=20)
    per = models.CharField(max_length=3)
    date = models.DateField()
    time = models.TimeField(blank=True, null=True)
    oopen = models.FloatField()
    high = models.FloatField()
    low = models.FloatField()
    close = models.FloatField()
    vol = models.BigIntegerField()

