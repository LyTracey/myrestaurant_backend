from django.apps import AppConfig


class MyrestaurantAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'myrestaurant_app'

    def ready(self) -> None:
        from .signals import model_handlers
