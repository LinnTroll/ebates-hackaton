from django.contrib import admin
from core.models import Airports, Cities, Countries


@admin.register(Airports)
class AirportsAdmin(admin.ModelAdmin):
    def get_country(self, item):
        return item.city.country.name

    def get_city(self, item):
        return item.city.name

    list_display = ('code', 'name', 'get_city', 'get_country')


@admin.register(Cities)
class CitiesAdmin(admin.ModelAdmin):
    list_display = ('name', 'country', 'timezone')


@admin.register(Countries)
class CountriesAdmin(admin.ModelAdmin):
    list_display = ('name', )
