from django.db import models


class Countries(models.Model):
    name = models.CharField(max_length=100)


class Cities(models.Model):
    name = models.CharField(max_length=100)
    country = models.ForeignKey('core.Country', on_delete=models.CASCADE)
    timezone = models.CharField()


class Airports(models.Model):
    name = models.CharField(max_length=100)
    city = models.ForeignKey('core.City', on_delete=models.CASCADE)
    country = models.ForeignKey('core.Country', on_delete=models.CASCADE)
    code = models.CharField(max_length=3)
    timezone = models.CharField()
