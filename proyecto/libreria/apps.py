from django.apps import AppConfig

class LibreriaConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'libreria'

    def ready(self):
        pass