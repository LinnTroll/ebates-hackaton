from django.contrib import admin
from core.models import Airports, Cities, Countries


@admin.register(Airports)
class AirportsAdmin(admin.ModelAdmin):
    def get_country(self, item):
        return item.city.country.name

    def get_city(self, item):
        return item.city.name

    list_display = ('code', 'name', 'get_city', 'get_country')
    search_fields = ('name', 'code')


@admin.register(Cities)
class CitiesAdmin(admin.ModelAdmin):
    def get_country(self, item):
        return item.country.name

    list_display = ('name', 'get_country', 'timezone')
    search_fields = ('name',)


@admin.register(Countries)
class CountriesAdmin(admin.ModelAdmin):
    list_display = ('name', )
    search_fields = ('name',)
