from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('albums/', include('albums.urls')),
    path('', lambda request: render(request, '404.html', status=404)),
]

if settings.DEBUG:  # doar în mod de dezvoltare
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)