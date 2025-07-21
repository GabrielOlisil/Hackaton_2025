from django.apps import AppConfig
import sys


class PlacesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'places'
    def ready(self):
        from . import scheduler
        management_commands = [
            'makemigrations',
            'migrate',
            'collectstatic',
            'shell',
            'createsuperuser'
        ]

        # Verifica se algum dos comandos acima está sendo executado.
        is_management_command = any(
            cmd in sys.argv for cmd in management_commands
        )

        # Inicia o agendador apenas se NÃO for um comando de gerenciamento.
        if not is_management_command:
            from . import scheduler
            scheduler.start()