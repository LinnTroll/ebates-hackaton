import os
import codecs
import csv
import urllib.request

from django.conf import settings
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from django.core.management.base import BaseCommand

from core.models import FlightCompany, Countries

API_URL = 'https://raw.githubusercontent.com/jpatokal/openflights/master/data/airlines.dat'


class Command(BaseCommand):

    def handle(self, *args, **options):
        FlightCompany.objects.all().delete()
        resp = urllib.request.urlopen(API_URL)
        csvfile = list(csv.reader(codecs.iterdecode(resp, 'utf-8')))
        total_cnt = len(csvfile)
        exists_iata_iamges = set()
        airlines_img_path = os.path.join(settings.MEDIA_ROOT, 'airlines')
        if os.path.isdir(airlines_img_path):
            exists_images_files = [x for x in os.listdir(airlines_img_path) if x.endswith('.png')]
            exists_iata_iamges = set([os.path.splitext(x)[0] for x in exists_images_files])
        icaos = set()
        for n, row in enumerate(csvfile):
            name = row[1].strip()
            iata = row[3].strip()
            icao = row[4].strip()
            country = row[6].strip()
            active = row[7].strip()

            if active != 'Y':
                continue

            if not iata or len(iata) != 2:
                continue

            if not icao or len(icao) != 3:
                continue

            if icao in icaos:
                continue

            try:
                country_obj = Countries.objects.get(name=country)
            except Countries.DoesNotExist:
                country_obj = None

            if country_obj:
                fc = FlightCompany(icao=icao, iata=iata, name=name, country=country_obj)
                fc.save()

                if iata not in exists_iata_iamges:
                    filename = f'{iata}.png'
                    img_url = f'https://images.kiwi.com/airlines/64x64/{filename}'

                    res = urllib.request.urlopen(img_url)
                    res_url = res.geturl()
                    if not res_url.endswith('airlines.png'):
                        img_temp = NamedTemporaryFile(delete=True)
                        img_temp.write(res.read())
                        img_temp.flush()

                        fc.image.save(filename, File(img_temp))

                print('# {:.2f}% {}'.format(n / total_cnt * 100, fc))