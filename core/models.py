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


class Product(models.Model):
    image = models.ImageField(upload_to='prod_images', blank=False, null=False)
    store = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    fmp_price = models.DecimalField(decimal_places=2, max_digits=10)
    regular_price = models.DecimalField(decimal_places=2, max_digits=10)
    cashback = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.store} - {self.name}'


class Recommend(models.Model):
    product = models.ForeignKey('core.Product', on_delete=models.CASCADE)
    # country = models.ManyToManyField(Countries)


class RecommendCountry(models.Model):
    country = models.ForeignKey('core.Countries', on_delete=models.CASCADE)
    recommend = models.ForeignKey('core.Recommend', on_delete=models.CASCADE)

# class Route(models.Model):
#     src = models.ForeignKey('core.Airports', related_name='route_src', on_delete=models.CASCADE)
#     dst = models.ForeignKey('core.Airports', related_name='route_dst', on_delete=models.CASCADE)
#
#     def __str__(self):
#         return f'{self.src} -> {self.dst}'
#
#
# class Flight(models.Model):
#     number = models.CharField(max_length=32)
#     route = models.ForeignKey('core.Route', on_delete=models.CASCADE)
#     company = models.ForeignKey('core.FlightCompany', on_delete=models.CASCADE)
#     date = models.DateTimeField()
#     duration = models.TimeField()
#     price = models.DecimalField(decimal_places=2, max_digits=10)
#
#     def __str__(self):
#         return f'{self.company} {self.number} / {self.route} / {self.date}'
