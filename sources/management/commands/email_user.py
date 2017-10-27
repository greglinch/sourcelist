from django.core.management.base import BaseCommand, CommandError
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from sesame import utils
from sources.models import Person
from sources.forms import SubmitForm
from sources.tokens import account_confirmation_token
from sourcelist.settings import PROJECT_NAME, EMAIL_SENDER, SITE_URL


def email_user(email_address, status):
    person = Person.objects.get(email_address=email_address)
    person_id = person.id

    fields = SubmitForm.Meta.fields ## abstracted to use same fields as the submission form
    fields.append('status') ## add status field bc it's not included in the SubmitForm and it's necessary for sending email
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
    confirm_token = account_confirmation_token.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    confirm_url = '{}/confirmation/{}/{}'.format(
        SITE_URL,
        uid.decode(),
        confirm_token
    )

    status = person['status']
    status_type = status.split('_')[0]
    
    message = ''

    if status_type == 'added':
        subject_title = 'You have been added as a source'
        if status == 'added_by_self':
            subject_title += 'yourself'
        elif status == 'added_by_other':
            subject_title += 'someone else'
        elif status == 'added_by_admin':
            subject_title += 'an admin'

        html_message = '\
            <p>Diverse Sources is a searchable database of underrepresented experts in the areas of science, health and the environment. Anyone who considers themselves underrepresented and is willing to respond to journalists on deadline is encouraged to join (including but not limited to appearance, ethnicity, gender expression, gender identity, language, mental health experience, nationality, physical abilities, race, religion, sex, sexual orientation, etc.).</p> \
            <p>This database aims to make it easy for journalists and others to include a wider range of backgrounds, experiences and perspectives in their work. By doing so, we can improve our coverage and better reflect the world we cover.</p> \
            <p>To confirm you would like be included in the {project_name} database and to confirm the following information is correct, please click here:</p> \
            <p>{confirm_url}</p> \
            <p>{person_info}</p> \
            <p>If the information is incorrect, please edit your entry:</p> \
            <p>{login_link}</p> \
            <p>View the database:</p> \
            <p>{site_url}</p>\
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

