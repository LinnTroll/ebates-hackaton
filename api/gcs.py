import mimetypes
import posixpath
from urllib.parse import urljoin

from django.conf import settings
from django.core.files.storage import default_storage
from django.http import (
    FileResponse, Http404, )
from django.utils.translation import gettext as _
from storages.backends.gcloud import GoogleCloudStorage
from storages.utils import setting


class GoogleCloudMediaStorage(GoogleCloudStorage):
    def __init__(self, *args, **kwargs):
        if not settings.MEDIA_URL:
            raise Exception('MEDIA_URL has not been configured')
        kwargs['bucket_name'] = setting('GS_BUCKET_NAME')
        super(GoogleCloudMediaStorage, self).__init__(*args, **kwargs)

    def url(self, name):
        return urljoin(settings.MEDIA_URL, name)


class GoogleCloudStaticStorage(GoogleCloudStorage):
    def __init__(self, *args, **kwargs):
        if not settings.STATIC_URL:
            raise Exception('STATIC_URL has not been configured')
        kwargs['bucket_name'] = setting('GS_BUCKET_NAME')
        super(GoogleCloudStaticStorage, self).__init__(*args, **kwargs)

    def url(self, name):
        return urljoin(settings.STATIC_URL, name)


def gcs_serve(request, path, document_root=None, show_indexes=False):
    path = posixpath.normpath(path).lstrip('/')
    if not default_storage.exists(path):
        raise Http404(_('"%(path)s" does not exist') % {'path': path})

    content_type, encoding = mimetypes.guess_type(str(path))
    content_type = content_type or 'application/octet-stream'
    response = FileResponse(default_storage.open(path, 'rb'), content_type=content_type)
    if encoding:
        response["Content-Encoding"] = encoding
    return response
