from __future__ import unicode_literals

from django.apps import AppConfig


class ReactivosSstAppConfig(AppConfig):
    name = 'reactivos_sst_app'
    verbose_name = "Reactivos SST/CBQ"


class CompoundsUpdateAppConfig(AppConfig):
    name = 'compounds_update_app'
    verbose_name = "Actualizar reactivos del CBQ"
