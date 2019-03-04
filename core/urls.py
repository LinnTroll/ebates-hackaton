from django.urls import path

from core.views import MainPage

app_name = 'core'

urlpatterns = [
    path('', MainPage.as_view(), name='main'),
]
