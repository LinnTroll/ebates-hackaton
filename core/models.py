from django.db import models


class Countries(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Cities(models.Model):
    name = models.CharField(max_length=100)
    country = models.ForeignKey('core.Countries', on_delete=models.CASCADE)
    timezone = models.CharField(max_length=32)

    class Meta:
        unique_together = (('name', 'country'),)

    def __str__(self):
        return f'{self.country} {self.name}'


class Airports(models.Model):
    code = models.CharField(max_length=3, primary_key=True)
    name = models.CharField(max_length=100)
    city = models.ForeignKey('core.Cities', on_delete=models.CASCADE)

    def __str__(self):
        return self.code


class FlightCompany(models.Model):
    icao = models.CharField(max_length=3, primary_key=True)
    iata = models.CharField(max_length=2)
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='airlines', blank=True, null=True)
    country = models.ForeignKey('core.Countries', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    @property
    def cashback(self):
        return sum(ord(s) for s in self.iata) % 5 + 1


class Store(models.Model):
    name = models.CharField(max_length=100)
    cashback = models.CharField(max_length=32)

    def __str__(self):
        return self.name


class Product(models.Model):
    image = models.ImageField(upload_to='prod_images', blank=False, null=False)
    store = models.ForeignKey('core.Store', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    fmp_price = models.DecimalField(decimal_places=2, max_digits=10)
    regular_price = models.DecimalField(decimal_places=2, max_digits=10)

    def __str__(self):
        return f'{self.store} - {self.name}'


class Recommend(models.Model):
    product = models.ForeignKey('core.Product', on_delete=models.CASCADE)


class RecommendCountry(models.Model):
    country = models.ForeignKey('core.Countries', on_delete=models.CASCADE)
    recommend = models.ForeignKey('core.Recommend', on_delete=models.CASCADE)
