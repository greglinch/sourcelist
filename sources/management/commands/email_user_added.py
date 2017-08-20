from django.core.management.base import BaseCommand, CommandError
from django.core.mail import send_mail
from sources.models import Person


def email_add_user(email_address):
    person = Person.objects.get(email_address=email_address)
    person_id = person.id
    person_url = '/admin/sources/person/{}/change/'.format(person_id)

    ## ABSTRACT (to settings_private)?
    subject = '[Science Sources] You have been added to the database'
    message = 'Please confirm your entry: <link for user {}>'.format(person_url)
    sender = 'news@mbloudoff.com'
    recipients = [email_address]
    # reply_email = sender

    send_mail(
        subject,
        message,
        sender,
        recipients,
        # reply_to=[reply_email],
        fail_silently=False,
    )


class Command(BaseCommand):
    help = 'Email new user when added.'

    def add_arguments(self, parser):
        ## required
        parser.add_argument('email', 
            help='Specify the user emamil.'
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
        email_add_user(email_address)

