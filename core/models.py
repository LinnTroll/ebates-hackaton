from django.db import models


class Countries(models.Model):
    name = models.CharField(max_length=100, unique=True)


class Cities(models.Model):
    name = models.CharField(max_length=100)
    country = models.ForeignKey('core.Countries', on_delete=models.CASCADE)
    timezone = models.CharField(max_length=32)

    class Meta:
        unique_together = (('name', 'country'),)


class Airports(models.Model):
    code = models.CharField(max_length=3, primary_key=True)
    name = models.CharField(max_length=100)
    city = models.ForeignKey('core.Cities', on_delete=models.CASCADE)
