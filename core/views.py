import datetime

import pytz
from django.core import serializers
from django.db.models import Q
from django.http import HttpResponse
from django.views.generic import (
    ListView,
)
from django.views.generic import TemplateView

from api.skypicker_api import get_flights
from core.forms import FlightSearchForm
from core.models import (
    Airports,
    FlightCompany,
)


class MainPage(TemplateView):
    template_name = 'core/main.html'

    # def get_flights(self):

    def get_context_data(self, **kwargs):
        context_data = super().get_context_data(**kwargs)
        form = FlightSearchForm(self.request.GET or None)
        if form.is_valid():
            src = form['src'].value()
            dst = form['dst'].value()
            date_from = datetime.datetime.strptime(form['date_from'].value(), '%d/%m/%Y').date()
            # date_to = datetime.datetime.strptime(form['date_to'].value(), '%d/%m/%Y').date()
            flights = list(get_flights(src, dst, date_from, date_from))
            companies_codes = set()
            sources_codes = set()
            for flight in flights:
                companies_codes.add(flight['company'])
                sources_codes.add(flight['src'])
            sources = {c.code: c for c in Airports.objects.filter(code__in=sources_codes)}
            companies = {c.iata: c for c in FlightCompany.objects.filter(iata__in=companies_codes)}
            for flight in flights:
                city = sources[flight['src']].city
                flight['company'] = companies[flight['company']]
                flight['city'] = city
                try:
                    local_tz = pytz.timezone(city.timezone)
                except pytz.exceptions.UnknownTimeZoneError:
                    local_tz = pytz.utc
                    flight['is_utc'] = True
                flight['local_date'] = flight['date'].astimezone(local_tz).replace(tzinfo=None)
            context_data['flights'] = flights
        context_data['form'] = form
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
