from django.db import models


class Country(models.Model):
    name = models.CharField(max_length=100)


class City(models.Model):
    name = models.CharField(max_length=100)
    country = models.ForeignKey('core.Country', on_delete=models.CASCADE)
    timezone = models.TimeField()


class Airport(models.Model):
    name = models.CharField(max_length=100)
    city = models.ForeignKey('core.City', on_delete=models.CASCADE)
    country = models.ForeignKey('core.Country', on_delete=models.CASCADE)
    code = models.CharField(max_length=3)
    timezone = models.TimeField()
