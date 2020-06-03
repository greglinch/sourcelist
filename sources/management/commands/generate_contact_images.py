from django.core.management.base import BaseCommand, CommandError

from sources.helpers import generate_image_from_text
from sources.models import Person


def generate_images():
    sources = Person.objects.all()

    for source in sources:
        source.save()


class Command(BaseCommand):
    help = 'Import sources from a csv file.'

    def handle(self, *args, **options):
        generate_images()
