from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User, Group
from django.contrib import messages
from sources.models import Person
import random


def set_related_user(email_address): # , person_id, user_existing
    person = Person.objects.get(email_address=email_address) # (id=person_id)
    # try:
    #     user_existing = User.objects.get(email=person.email_address)
    # except:
    #     user_existing = False
    user = person.related_user
    if user:
        ## update User fields based on the Person
        user.email = person.email_address
        user.first_name = person.first_name
        user.last_name = person.last_name
        user.save()
    else:
        username = '{}{}'.format(person.first_name, person.last_name).lower().replace('-','').replace('\'','').replace(' ', '')
        # see if someone else already has this username
        username_exists = User.objects.filter(username=username).exists()
        # if the username exists, append person id to make it unique
        if username_exists:
            username += str(person.id)
        choices = 'abcdefghijklmnopqrstuvwxyz0123456789'
        middle_choices = choices + '!@#$%^&*(-_=+)'
        password = \
            ''.join([random.SystemRandom().choice(choices) for i in range(1)]) + \
            ''.join([random.SystemRandom().choice(middle_choices) for i in range(23)]) + \
            ''.join([random.SystemRandom().choice(choices) for i in range(1)])
        user = User.objects.create_user(username, password=password)
        user.email = person.email_address
        user.first_name = person.first_name
        user.last_name = person.last_name
        user.save()
        ## add new User to a group
        # try:
        # if not user.last_login:
            ## get the group
        group = Group.objects.get(name__contains='change source')
        ## add the user to that group
        group.user_set.add(user)
        ## set the user as staff
        user.is_staff = True
        user.save()
        # except:
        #     message = 'unable to associate {} with {}'.format(user, group)
            ## email to admin?
        ## associate the new User with the new Person
        # try:
        person.related_user = user
        person.save()
        # except:
        #     message = 'unable to associate {} with {}'.format(user_existing, person)
            ## email to admin?

class Command(BaseCommand):
    help = 'Set the related user for a Person.'

    def add_arguments(self, parser):
        ## required
        parser.add_argument('email', 
            help='Specify the user email.'
        )

        # optional
        # parser.add_argument('-e' '--existing',
        #     action='store_true',
        #     # type=str,
        #     dest='existing',
        #     default=False,
        #     help='Specific user exists or not.'
        # )

    def handle(self, *args, **options):
        ## unpack args
        email_address = options['email']
        # user_existing = options['existing']

        ## call the function
        # set_related_user(email_address, user_existing)
        set_related_user(email_address)

