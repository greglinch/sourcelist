from django.core.management.base import BaseCommand, CommandError

from sources.helpers import generate_image_from_text
from sources.models import Person


def generate_images():
    sources = Person.objects.all()

    for source in sources:
        source_id = source.id

        # email address
        # try:
        image_location = generate_image_from_text(
            source_id,
            source.email_address,
            'email_address'
        )
        source.email_address_image = image_location
        source.save()
        # except:
        #     print(f'Failed: email_address - {source_id}')

        # phone number primary
        # try:
        image_location = generate_image_from_text(
            source_id,
            source.phone_number_primary,
            'phone_number_primary'
        )
        source.phone_number_primary_image = image_location
        source.save()
        # except:
            # print(f'Failed: phone_number_primary - {source_id}')

        # phone number secondary
        # try:
        if source.phone_number_secondary:
            image_location = generate_image_from_text(
                source.id,
                source.phone_number_secondary,
                'phone_number_secondary'
            )
            source.phone_number_secondary_image = image_location
            source.save()
        else:
            print(f'N/A: phone_number_secondary - {source_id}')
        # except:
        #     print(f'Failed: phone_number_secondary - {source_id}')


class Command(BaseCommand):
    help = 'Import sources from a csv file.'

    def handle(self, *args, **options):
        generate_images()
