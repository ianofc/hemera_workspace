from django.apps import AppConfig

class CoreConfig(AppConfig):
    label = 'core'
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

    def ready(self):
        import core.signals
