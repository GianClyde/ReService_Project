from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.base import RedirectView
urlpatterns = [
    path('admin-site/', RedirectView.as_view(url='/admin'),name='admin'),

    path("admin/", admin.site.urls),
    path("", include('main.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
