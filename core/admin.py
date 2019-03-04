from django.contrib import admin
from django.utils.safestring import mark_safe
from core.models import Airports, Cities, Countries, FlightCompany


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
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(FlightCompany)
class FlightCompanyAdmin(admin.ModelAdmin):
    def img(self, item):
        if item.image:
            return mark_safe(f'<img src="{item.image.url}" height="16" />')

        return None


    list_display = ('icao', 'img', 'iata', 'name', 'country')
    search_fields = ('icao', 'iata', 'name',)

# @admin.register(Route)
# class RouteAdmin(admin.ModelAdmin):
#     list_display = ('src', 'dst')
#
#
# @admin.register(Flight)
# class FlightAdmin(admin.ModelAdmin):
#     list_display = ('number', 'route', 'company', 'price', 'duration', 'date')
