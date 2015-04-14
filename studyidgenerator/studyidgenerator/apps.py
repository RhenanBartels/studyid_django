from django.apps import AppConfig as BaseAppConfig
from django.utils.importlib import import_module


class AppConfig(BaseAppConfig):

    name = "studyidgenerator"

    def ready(self):
        import_module("studyidgenerator.receivers")
