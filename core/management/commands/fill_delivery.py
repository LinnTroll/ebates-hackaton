import random
from itertools import product

from django.core.management.base import BaseCommand

from core.models import Countries, Store, StoreDelivery


class Command(BaseCommand):
    def get_random_price(self, src, dst):
        if random.randint(0, 10) != 0:
            return None

        if src == dst:
            base = random.randint(2, 10)
        else:
            if random.randint(0, 10) == 0:
                base = random.randint(8, 14)
            elif random.randint(0, 5) == 0:
                base = random.randint(14, 25)
            else:
                base = random.randint(25, 100)
        cents = 0
        if random.randint(0, 10) == 0:
            cents = random.randint(1, 99)
        elif random.randint(0, 3) == 0 and str(base)[-1] == '9':
            cents = 99
        elif random.randint(0, 20) == 0:
            cents = 50
        elif random.randint(0, 20) == 0:
            cents = 33
        return base + cents / 100

    def handle(self, *args, **options):
        StoreDelivery.objects.all().delete()
        stores = Store.objects.all()
        for store in stores:
            print('Process store:', store)
            deliveries = []
            countries = Countries.objects.all()
            combinations = product(countries, countries)
            for src, dst in combinations:
                price = self.get_random_price(src, dst)
                if price is None:
                    continue

                deliveries.append(StoreDelivery(
                    store=store,
                    src=src,
                    dst=dst,
                    price=price,
                ))
            StoreDelivery.objects.bulk_create(deliveries)
