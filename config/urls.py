from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("home.urls")),
    path("user/", include("user.urls")),
    path("shop/", include("shop.urls")),
    path("panel/", include("panel.urls")),
    path("contact/", include("contact.urls")),
    path("api/", include("store.urls")),
]

# DEBUG = True bo‘lganda localda ishlaydi
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
