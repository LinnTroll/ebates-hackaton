import datetime
import json
from urllib.parse import urlencode

import pytz
from django.core import serializers
from django.db.models import Q, Min
from django.http import HttpResponse
from django.views.generic import (
    ListView,
)
from django.views.generic import TemplateView

from api.skypicker_api import get_flights
from core.forms import FlightSearchForm
from core.models import (
    Store,
    Airports,
    FlightCompany,
    StoreDelivery,
)


class MainPage(TemplateView):
    def dispatch(self, request, *args, **kwargs):
        self.flight_form = FlightSearchForm(request.GET or None)
        self.request_data = dict(self.request.GET.items())
        return super().dispatch(request, *args, **kwargs)

    def get_template_names(self):
        if self.flight_form.is_valid():
            return 'core/flights.html'

        return 'core/main.html'

    def json_flights_defaults(self, item):
        if isinstance(item, datetime.datetime):
            return str(item)

    def get_flights(self):
        if self.flight_form.is_valid():
            src = self.flight_form['src'].value()
            dst = self.flight_form['dst'].value()
            if 'back' in self.request_data:
                date_to = datetime.datetime.strptime(self.flight_form['date_to'].value(), '%d/%m/%Y').date()
                flights = list(get_flights(dst, src, date_to, date_to))
            else:
                date_from = datetime.datetime.strptime(self.flight_form['date_from'].value(), '%d/%m/%Y').date()
                flights = list(get_flights(src, dst, date_from, date_from))
            companies_codes = set()
            sources_codes = set()
            for flight in flights:
                companies_codes.add(flight['company'])
                sources_codes.add(flight['src'])
            sources = {c.code: c for c in Airports.objects.filter(code__in=sources_codes)}
            companies = {c.iata: c for c in FlightCompany.objects.filter(iata__in=companies_codes)}
            for flight in flights:
                flight['duration'] = str(flight['duration'])[:-3]
                flight_json = json.dumps(flight, default=self.json_flights_defaults)
                # flight['json'] = json.dumps(flight, default=self.json_flights_defaults)
                city = sources[flight['src']].city
                flight['company'] = companies[flight['company']]
                flight['city'] = city
                try:
                    local_tz = pytz.timezone(city.timezone)
                except pytz.exceptions.UnknownTimeZoneError:
                    local_tz = pytz.utc
                    flight['is_utc'] = True
                flight['local_date'] = flight['date'].astimezone(local_tz).replace(tzinfo=None)

                if self.request.GET.get('roundTrip') == 'true':
                    if 'back' in self.request_data:
                        buy_url = '/buy?{}'.format(urlencode({
                            'bck_flight': flight_json,
                            **self.request_data,
                        }))
                    else:
                        buy_url = '/?{}'.format(urlencode({
                            'fwd_flight': flight_json,
                            **self.request_data,
                            **{'back': True}
                        }))
                else:
                    buy_url = '/buy/?{}'.format(urlencode({
                        'fwd_flight': flight_json,
                        **self.request_data
                    }))
                flight['buy_url'] = buy_url
            return flights

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['flights'] = self.get_flights()
        context_data['form'] = self.flight_form
        return context_data


class BuyPage(TemplateView):
    template_name = 'core/buy.html'
    fwd_flight = None
    bck_flight = None

    def dispatch(self, request, *args, **kwargs):
        raw_fwd_flight = request.GET.get('fwd_flight')
        if raw_fwd_flight:
            self.fwd_flight = json.loads(raw_fwd_flight)
        raw_bck_flight = request.GET.get('bck_flight')
        if raw_bck_flight:
            self.bck_flight = json.loads(raw_bck_flight)
        return super().dispatch(request, *args, **kwargs)

    def get_suggest_deliveries(self):
        src_airport = Airports.objects.get(code=self.fwd_flight['src'])
        dst_airport = Airports.objects.get(code=self.fwd_flight['dst'])
        src_country = src_airport.city.country
        dst_country = dst_airport.city.country
        if src_country == dst_country:
            return

        src_deliveries = StoreDelivery.objects \
            .filter(dst=src_country) \
            .exclude(src=src_country) \
            .values('store_id') \
            .annotate(Min('price'))

        src_deliveries_map = {d['store_id']: d for d in src_deliveries}

        dst_deliveries = StoreDelivery.objects \
            .filter(dst=dst_country) \
            .exclude(src=dst_country) \
            .values('store_id') \
            .annotate(Min('price'))

        suggestions = []
        stores_ids = set()
        for dst_delivery in dst_deliveries:
            src_delivery = src_deliveries_map.get(dst_delivery['store_id'])
            if not src_delivery:
                continue

            src_price = src_delivery['price__min']
            dst_price = dst_delivery['price__min']
            if src_price <= dst_price:
                continue

            store_id = dst_delivery['store_id']
            stores_ids.add(store_id)
            suggestions.append({
                'store_id': store_id,
                'src_price': f'{src_price:.2f}',
                'dst_price': f'{dst_price:.2f}',
                'dst_country': dst_country,
            })

        stores_map = {s.pk: s for s in Store.objects.filter(pk__in=stores_ids)}
        for suggest in suggestions:
            suggest['store'] = stores_map[suggest['store_id']]

        return suggestions

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        context_data['fwd_flight'] = self.fwd_flight
        context_data['bck_flight'] = self.bck_flight
        context_data['suggest_deliveries'] = self.get_suggest_deliveries()
        return context_data


class AirportsListView(ListView):
    model = Airports

    def get_queryset(self):
        q_param = self.request.GET.get('term')
        q_limit = int(self.request.GET.get('limit', 10))
        if q_limit > 100:
            q_limit = 100
        if q_param and len(q_param) > 1:
            queryset = super().get_queryset()
            queryset = queryset.filter(
                Q(city__name__icontains=q_param) |
                Q(name__icontains=q_param) |
                Q(code=q_param.upper())
            )
            return queryset[:q_limit]

        return self.model.objects.none()

    def render_to_response(self, context, **response_kwargs):
        resp = HttpResponse(serializers.serialize('json', self.object_list), content_type='application/json')
        return resp
