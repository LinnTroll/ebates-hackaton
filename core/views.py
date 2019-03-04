import json

from django.db.models import Q
from django.http import Http404
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.text import slugify
from django.views.generic import (
    ListView,
    UpdateView,
    CreateView,
    View,
)

from core.models import (
    Countries,
    Cities,
    Airports,
)


class AirportsListView(ListView):
    model = Airports
    type_filtering = True

    def get_queryset(self):
        queryset = super().get_queryset()
        q_param = self.request.GET.get('q')
        if q_param:
            queryset = queryset.filter(slug__contains=slugify(q_param))
        filters = []
        if filters:
            queryset = queryset.filter(store_type__in=filters)
        return queryset.select_related(
            'code',
            'name',
            'city',
            'country',
            'timezone',
        )
