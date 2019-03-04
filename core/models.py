from django.db import models


class Countries(models.Model):
    name = models.CharField(max_length=100, unique=True)


class Cities(models.Model):
    name = models.CharField(max_length=100, unique=True)
    country = models.ForeignKey('core.Country', on_delete=models.CASCADE)
    timezone = models.CharField(max_length=32)


class Airports(models.Model):
    code = models.CharField(max_length=3, unique=True, primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    city = models.ForeignKey('core.City', on_delete=models.CASCADE)
