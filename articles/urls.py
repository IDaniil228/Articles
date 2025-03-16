from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from  articles import  settings

urlpatterns = [
    path("", include("web.urls")),
    path("api/", include("api.urls")),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)