from django.core.management.base import BaseCommand, CommandError
from django.core.mail import send_mail
# from django.utils import timezone
from sources.models import Person
from sourcelist.settings import PROJECT_NAME, EMAIL_SENDER, SITE_URL


def email_admin():
    path = '/admin/sources/sourceforadmin/'
    path += '?approved_by_admin__exact=0'
    # path += '&created={}'.format(timezone.now().date())
    admin_url = SITE_URL + path

    unapproved_sources = Person.objects.filter(
        role='source',
        approved_by_admin=False,
        declined_by_admin=False
    )
    unapproved_count = unapproved_sources.count()
    
    if unapproved_count:
        plural = ''
        if unapproved_count > 1:
            plural = 's'
        source_list_items = ''
        for source in unapproved_sources:
            source_link = '{}/admin/sources/sourceforadmin/{}/change/'.format(SITE_URL, source.id)
            item = '<li><a href="{}">{}</a></li>'.format(source_link, source)
            source_list_items += item

        subject = '[{}] {} sources pending approval'.format(PROJECT_NAME, unapproved_count)
        message = ''
        sender = EMAIL_SENDER
        recipients = [EMAIL_SENDER]
        html_message = '<p>The following source{} need to be reviewed:</p>{}'.format(plural, source_list_items)

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
    help = 'Email admin to approve new user.'

    def handle(self, *args, **options):
        email_admin()
