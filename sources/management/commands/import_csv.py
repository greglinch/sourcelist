from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User, Group
from sources.models import Person
import random


def import_csv():
    # import code
    call_command('set_related_user', email_address)
    call_command('email_user', email_address, status)

class Command(BaseCommand):
    help = 'Import sources from a csv file.'

    # def add_arguments(self, parser):
    #     ## required
    #     parser.add_argument('email', 
    #         help='Specify the user email.'
    #     )

        ## optional
        # parser.add_argument('-t' '--test',
        #     action='store_true',
        #     # type=str,
        #     dest='test',
        #     default=False,
        #     help="Specific whether it's a test or not"
        # )

    def handle(self, *args, **options):
        ## unpack args
        # email_address = options['email']

        ## call the function
        import_csv()

