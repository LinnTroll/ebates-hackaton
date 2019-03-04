from django.urls import path
from django.conf.urls.static import static
from django.conf import settings

from core.views import (
    AirportsListView,
    MainPage,
)

app_name = 'core'

urlpatterns = [
    path('', MainPage.as_view(), name='main'),
    path('api/airports/list/', AirportsListView.as_view(), name='airport_list'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
