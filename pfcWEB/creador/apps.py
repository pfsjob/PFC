from django.apps import AppConfig


class CreadorConfig(AppConfig):
    name = 'creador'
    def ready(self):
        import creador.signals


