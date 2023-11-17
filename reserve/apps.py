# reserve/apps.py

from django.apps import AppConfig

class ReserveConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'reserve'

# Register the AppConfig class with the application.
default_app_config = 'reserve.ReserveConfig'
