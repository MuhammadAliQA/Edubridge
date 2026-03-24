import os
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import Http404, JsonResponse
from django.shortcuts import redirect
from django.contrib.auth import get_user_model

def handler404_view(request, exception):
    from django.shortcuts import render
    return render(request, '404.html', status=404)

handler404 = handler404_view

def blocked_admin(_request):
    raise Http404()

def favicon_redirect(_request):
    return redirect("/static/favicon.svg", permanent=True)

def healthz(_request):
    admin_path = os.environ.get("ADMIN_PATH")
    if admin_path is None:
        admin_path = "admin/" if settings.DEBUG else "secure-admin/"

    User = get_user_model()
    return JsonResponse(
        {
            "ok": True,
            "debug": settings.DEBUG,
            "admin_path": admin_path,
            "render_git_commit": os.environ.get("RENDER_GIT_COMMIT"),
            "has_bootstrap_admin_token": bool((os.environ.get("BOOTSTRAP_ADMIN_TOKEN") or "").strip()),
            "bootstrap_superuser_enabled": os.environ.get("BOOTSTRAP_SUPERUSER") == "True",
            "superuser_count": User.objects.filter(is_superuser=True).count(),
        }
    )

ADMIN_PATH = os.environ.get('ADMIN_PATH')
if ADMIN_PATH is None:
    ADMIN_PATH = 'admin/' if settings.DEBUG else 'secure-admin/'
if not ADMIN_PATH.endswith('/'):
    ADMIN_PATH += '/'

urlpatterns = [
    path('healthz/', healthz),
    path('favicon.ico', favicon_redirect),
    path('admin/', blocked_admin) if (not settings.DEBUG and ADMIN_PATH != 'admin/') else path('admin/', admin.site.urls),
    path('', include('courses.urls')),
    path('', include('accounts.urls')),
]

if not (settings.DEBUG and ADMIN_PATH == 'admin/'):
    urlpatterns.insert(1, path(ADMIN_PATH, admin.site.urls))

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
