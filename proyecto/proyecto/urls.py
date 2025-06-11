from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.defaults import page_not_found, server_error, permission_denied, bad_request

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('libreria.urls')),
]

# Sirve multimedia
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Sirve estáticos en desarrollo
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

handler404 = page_not_found
handler500 = server_error
handler403 = permission_denied
handler400 = bad_request