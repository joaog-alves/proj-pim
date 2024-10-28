# benessere/apps.py
from django.apps import AppConfig

class BenessereConfig(AppConfig):
    name = 'benessere'

    def ready(self):
        # Importa os sinais quando o aplicativo está pronto
        import benessere.signals
