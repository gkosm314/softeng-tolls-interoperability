from django.apps import AppConfig


class BackendConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'backend'

    # Register signals here
    def ready(self):
        # Implicitly connect a signal handlers decorated with @receiver.
        from . import signals