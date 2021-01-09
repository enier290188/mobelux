from django.apps import AppConfig


class SecurityConfig(AppConfig):
    name = 'backend.security'
    verbose_name = 'Security'

    def ready(self):
        from backend.security import signals
