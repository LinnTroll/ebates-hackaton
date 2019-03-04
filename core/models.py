from django.db import models


class Countries(models.Model):
    name = models.CharField(max_length=100, unique=True)


class Cities(models.Model):
    name = models.CharField(max_length=100, unique=True)
    country = models.ForeignKey('core.Country', on_delete=models.CASCADE)
    timezone = models.CharField(max_length=32)

    class Meta:
        unique_together = (('name', 'country'),)


class Airports(models.Model):
    code = models.CharField(max_length=3, primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    city = models.ForeignKey('core.City', on_delete=models.CASCADE)
