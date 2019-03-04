from django.urls import path

from core.views import (
    AirportsListView,
)

app_name = 'core'

urlpatterns = [
    path('', AirportsListView.as_view(), name='airport_list'),
]
