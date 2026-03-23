import os
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import Http404

def handler404_view(request, exception):
    from django.shortcuts import render
    return render(request, '404.html', status=404)

handler404 = handler404_view

def blocked_admin(_request):
    raise Http404()

ADMIN_PATH = os.environ.get('ADMIN_PATH')
if ADMIN_PATH is None:
    ADMIN_PATH = 'admin/' if settings.DEBUG else 'secure-admin/'
if not ADMIN_PATH.endswith('/'):
    ADMIN_PATH += '/'

urlpatterns = [
    path('admin/', blocked_admin) if (not settings.DEBUG and ADMIN_PATH != 'admin/') else path('admin/', admin.site.urls),
    path('', include('courses.urls')),
    path('', include('accounts.urls')),
]

if not (settings.DEBUG and ADMIN_PATH == 'admin/'):
    urlpatterns.insert(1, path(ADMIN_PATH, admin.site.urls))

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
