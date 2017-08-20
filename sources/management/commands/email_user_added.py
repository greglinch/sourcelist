from django.core.management.base import BaseCommand, CommandError
from django.core.mail import send_mail
from sources.models import Person
from sourcelist.settings import PROJECT_NAME, EMAIL_SENDER


def email_add_user(email_address, status):
    person = Person.objects.get(email_address=email_address)
    person_id = person.id
    person_url = '/admin/sources/person/{}/change/'.format(person_id)

    subject_title = 'You have been added as a source by '
    if status = 'submitted_by_self':
        subject_title += 'yourself'
    elif status = 'submitted_by_other':
        subject_title += 'someone else'
    elif status = 'submitted_by_admin':
        subject_title += 'an admin'

    subject = '[{}] {}'.format(PROJECT_NAME, subject_title)
    message = 'Please confirm your entry: <link for user {}>'.format(person_url)
    sender = EMAIL_SENDER
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

        parser.add_argument('status',
            help='Specify the status.'
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
        status = options['status']

        ## call the function
        email_add_user(email_address, status)

