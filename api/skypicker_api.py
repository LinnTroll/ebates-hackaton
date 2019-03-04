import datetime
import json
from urllib.parse import urlencode, urlsplit, urlunsplit
from urllib.request import urlopen

API_URL = 'https://api.skypicker.com/flights'


def build_url(src, dst, date_from, date_to):
    scheme, netloc, path, *_ = urlsplit(API_URL)
    qs = urlencode({
        'flyFrom': src,
        'to': dst,
        'dateFrom': date_from.strftime('%d/%m/%Y'),
        'dateTo': date_to.strftime('%d/%m/%Y'),
        'curr': 'USD',
        'locale': 'us',
        'partner': 'picky',
    })
    return urlunsplit((scheme, netloc, path, qs, None))


def get_flight(raw_flight):
    if len(raw_flight['airlines']) != 1:
        return None

    return {
        'src': raw_flight['flyFrom'],
        'dst': raw_flight['flyTo'],
        'number': str(raw_flight['route'][0]['flight_no']),
        'company': raw_flight['airlines'][0],
        'date': datetime.datetime.utcfromtimestamp(raw_flight['dTimeUTC']),
        'duration': datetime.timedelta(seconds=raw_flight['duration']['total']),
        'price': raw_flight['price'],
    }


def get_flights(src, dst, date_from, date_to):
    url = build_url(src, dst, date_from, date_to)
    print(url)
    raw_flights = json.loads(urlopen(url).read())
    for raw_flight in raw_flights['data']:
        flight = get_flight(raw_flight)
        if flight:
            yield flight
