from django.core import serializers
from django.db.models import Q
from django.http import HttpResponse
from django.views.generic import (
    ListView,
)

from core.models import (
    Airports,
)

from django.views.generic import TemplateView


class MainPage(TemplateView):
    template_name = 'core/main.html'


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
