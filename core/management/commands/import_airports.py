import urllib.request
from django.core.management.base import BaseCommand, CommandError
import csv
import codecs
from core.models import Airports, Cities, Countries

API_URL = 'https://raw.githubusercontent.com/jpatokal/openflights/master/data/airports.dat'


class Command(BaseCommand):

    def handle(self, *args, **options):
        Airports.objects.all().delete()
        Cities.objects.all().delete()
        Countries.objects.all().delete()

        resp = urllib.request.urlopen(API_URL)
        csvfile = list(csv.reader(codecs.iterdecode(resp, 'utf-8')))
        total_cnt = len(csvfile)

        countries = {}
        cities = {}
        airports = []

        for n, row in enumerate(csvfile):
            airport_name = row[1].strip()
            city_name = row[2].strip()
            country_name = row[3].strip()
            airport_code = row[4].strip()
            city_tz = row[11].strip()

            if country_name not in countries:
                countries[country_name] = Countries(name=country_name)
            country = countries[country_name]

        Countries.objects.bulk_create(countries.values())
        countries = {c.name: c for c in Countries.objects.all()}

        for n, row in enumerate(csvfile):
            airport_name = row[1].strip()
            city_name = row[2].strip()
            country_name = row[3].strip()
            airport_code = row[4].strip()
            city_tz = row[11].strip()

            if not city_name or city_name == '\\N':
                continue

            country = countries[country_name]
            if city_name not in cities:
                cities[(country_name, city_name)] = Cities(
                    name=city_name,
                    timezone=city_tz,
                    country=country,
                )

        Cities.objects.bulk_create(cities.values())
        cities = {(c.country.name, c.name): c for c in Cities.objects.all()}


        for n, row in enumerate(csvfile):
            airport_name = row[1].strip()
            city_name = row[2].strip()
            country_name = row[3].strip()
            airport_code = row[4].strip()
            city_tz = row[11].strip()

            if not airport_code or airport_code == '\\N':
                continue

            country = countries[country_name]
            city = cities.get((country_name, city_name))
            if city:
                airports.append(Airports(
                    code=airport_code,
                    name=airport_name,
                    city=city,
                ))

        print('# Write airports...')
        Airports.objects.bulk_create(airports)
        print('# Done')
