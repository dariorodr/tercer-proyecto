from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from libreria.views import custom_404  # Importar el manejador personalizado

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('libreria.urls')),
]

# Sirve multimedia
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Sirve estáticos en desarrollo
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Manejadores de errores personalizados
handler404 = 'libreria.views.custom_404'
handler500 = 'django.views.defaults.server_error'
handler403 = 'django.views.defaults.permission_denied'
handler400 = 'django.views.defaults.bad_request'