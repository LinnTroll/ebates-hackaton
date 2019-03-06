from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import (
    path,
    include,
)

from api.gcs import gcs_serve

urlpatterns = [
    path('', include('core.urls')),
    path('admin/', admin.site.urls),
]

if settings.IS_DEVELOP:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
else:
    urlpatterns += static(settings.MEDIA_URL, view=gcs_serve, document_root=settings.MEDIA_ROOT)
