from __future__ import unicode_literals

from django.apps import AppConfig
from watson import search as watson


class SourcesConfig(AppConfig):
    name = 'sources'

    def ready(self):
        Person = self.get_model('Person')
        watson.register(Person)