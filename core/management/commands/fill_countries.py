import json
from urllib.error import HTTPError
from urllib.parse import urlsplit, urlunsplit, urlencode
from urllib.request import urlopen

from django.core.management.base import BaseCommand

from core.models import Countries

API_URL = 'https://restcountries.eu/rest/v2/name'


class Command(BaseCommand):

    def build_api_url(self, name):
        scheme, netloc, path, *_ = urlsplit(API_URL)
        path = f'{path}/{name}'
        qs = urlencode({'fullText': 'true'})
        return urlunsplit((scheme, netloc, path, qs, None))

    def handle(self, *args, **options):
        countries = Countries.objects.all()
        for country in countries:
            url = self.build_api_url(country.name)
            try:
                resp = urlopen(url)
            except HTTPError as exc:
                print(f'Skip "{country.name}" (EXC: {exc})')
                continue

            if resp.status != 200:
                print(f'Skip "{country.name}" (STATUS: {resp.status})')
                continue

            data = json.loads(resp.read())
            if len(data) != 1:
                print(f'Skip "{country.name}" (LEN: {len(data)})')
                continue

            country.alpha2 = data[0]['alpha2Code']
            country.save()

            print(country.name, country.alpha2)
