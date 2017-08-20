from django.core.management.base import BaseCommand, CommandError
from django.core.mail import send_mail
from django.contrib.auth.models import User
from sources.models import Person
import random


def set_related_user(email_address): # , person_id
    obj = Person.objects.get(email_address=email_address) # (id=person_id)
    try:
        user_existing = User.objects.get(email=obj.email_address)
    except:
        user_existing = False
    if user_existing:
        obj.related_user = user_existing
    else:
        username = '{}{}'.format(obj.first_name, obj.last_name).lower().replace('-','')
        choices = 'abcdefghijklmnopqrstuvwxyz0123456789'
        middle_choices = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
        password = \
            ''.join([random.SystemRandom().choice(choices) for i in range(1)]) + \
            ''.join([random.SystemRandom().choice(middle_choices) for i in range(23)]) + \
            ''.join([random.SystemRandom().choice(choices) for i in range(1)])
        user_new = User.objects.create_user(username, password=password)
        user_new.email = obj.email_address
        user_new.first_name = obj.first_name
        user_new.last_name = obj.last_name
        user_new.save()


class Command(BaseCommand):
    help = 'Set the related user for a Person.'

    def add_arguments(self, parser):
        ## required
        parser.add_argument('email', 
            help='Specify the user email.'
        )

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
        email_address = options['email']

        ## call the function
        set_related_user(email_address)

