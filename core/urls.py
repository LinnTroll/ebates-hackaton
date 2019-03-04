from django.urls import path

from core.views import (
    AirportsListView,
    MainPage,
)

app_name = 'core'

urlpatterns = [
    path('', MainPage.as_view(), name='main'),
    path('api/airports/list/', AirportsListView.as_view(), name='airport_list'),
]
