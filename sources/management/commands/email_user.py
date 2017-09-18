from django.core.management.base import BaseCommand, CommandError
from django.core.mail import send_mail
from django.contrib.auth.models import User
from sesame import utils
from sources.models import Person
from sources.forms import SubmitForm
from sourcelist.settings import PROJECT_NAME, EMAIL_SENDER, SITE_URL


def email_user(email_address, status):
    person = Person.objects.get(email_address=email_address)
    person_id = person.id

    fields = SubmitForm.Meta.fields ## abstracted to use same fields as the submission form
    person = Person.objects.filter(email_address=email_address).values(*fields).exclude()[0]
    person_info = '<table>'
    spaces = '&nbsp;' * 5
    ## loop thru and unpack values
    for key, value in person.items():
        if value:
            new_key = key.title().replace('_', ' ')
            person_info += '\
                <tr> \
                    <td><b>{}</b>:</td> \
                    <td>{}</td> \
                    <td>{}</td>\
                </tr>'.format(
                    new_key, 
                    spaces, 
                    value
                )
    person_info += '</table>'

    admin_url = '{}/admin/sources/person/{}/change/'.format(SITE_URL, person_id)

    ## django-sesame bits for magic link
    user = User.objects.get(email=email_address)
    # login_token = utils.get_query_string(user) ## using their URL
    login_token = utils.get_parameters(user) ## making your own URL
    login_link = '{}?method=magic&url_auth_token={}'.format(admin_url, login_token['url_auth_token']) ## change from admin url to live url?

    ## confirmation url (for both user and admin?)
    confirm_token = '<confirm_token_here>' ## UPDATE
    confirm_url = '{}/confirmation/{}'.format(SITE_URL, confirm_token)

    status = person['status']
    status_type = status.split('_')[0]
    
    message = ''

    if status_type == 'added':
        subject_title = 'You have been added as a source by '
        if status == 'added_by_self':
            subject_title += 'yourself'
        elif status == 'added_by_other':
            subject_title += 'someone else'
        elif status == 'added_by_admin':
            subject_title += 'an admin'

        html_message = 'To confirm you would like be included in the {project_name} database and to confirm the following information is correct, please click here: <br><br> {confirm_url} <br><br> \
            {person_info} <br><br> \
            If the information if incorrect, please edit your entry: <br><br> {login_link} <br><br>View the database:<br><br> {site_url}\
            '.format(
                project_name=PROJECT_NAME,
                confirm_url=confirm_url,
                person_info=person_info,
                login_link=login_link,
                site_url=SITE_URL
            )
    # elif status_type == 'approved':
    #     subject_title = 'You have been approved as a source!'
    #     html_message = 'Congratulations! Your entry has been approved and now be viewed or updated by you here: {}'.format(person_url)

    subject = '[{}] {}'.format(PROJECT_NAME, subject_title)
    sender = EMAIL_SENDER
    recipients = [email_address]
    # reply_email = sender

    send_mail(
        subject,
        message,
        sender,
        recipients,
        # reply_to=[reply_email],
        html_message=html_message,
        fail_silently=False,
    )


class Command(BaseCommand):
    help = 'Email new user when added.'

    def add_arguments(self, parser):
        ## required
        parser.add_argument('email', 
            help='Specify the user email.'
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
        email_user(email_address, status)

