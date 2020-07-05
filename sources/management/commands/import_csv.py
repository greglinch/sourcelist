import csv
from datetime import datetime
import sys

from django.core.management.base import BaseCommand, CommandError
from django.core.management import call_command
from django.contrib.auth.models import User, Group
from django.utils import timezone

from sourcelist.settings import TEST_ENV
from sources.models import Person


def create_person(row_num, failed_rows, data_dict):
    """
    Create a Person in the system as part of the import process. Works for
    both import file types.
    """
    email_address = data_dict['email_address']
    # check if the person already exists:
    person_exists = Person.objects.filter(email_address=email_address).exists()
    if person_exists == False:
        try:
            obj, created = Person.objects.update_or_create(**data_dict)
        except Exception as e:
            failed_rows += 1
            message = f'Row {counter} for {email_address}: {e}\n'
            print(message)
    # except:
        # failed_rows.append(counter)
    # try:
    #     obj, created = Person.objects.create(**csv_to_model)
    # except:
    #     message = 'Create person' + str(sys.exc_info())
    #     print(message)
    ## set the related user and email them
    try:
        call_command('set_related_user', email_address)
    except:
        message = 'Set related user: ' + str(sys.exc_info())
        print(message)
    if TEST_ENV:
        send_user_email = input('Do you want to send user confirmation email? T/F ')
        if 'T' in send_user_email:
            try:
                print('This is when it would send')
                # call_command('email_user', email_address, status)
            except:
                message = 'Email user:' + str(sys.exc_info())
                print(message)


def import_csv(csv_file):
    ## start
    start_time = datetime.now()
    start_message = '\nStarted import:\t {}\n'.format(start_time)
    message = start_message
    print(message)

    # row_count = sum(1 for row in csv_reader) # need to assign this
    # message = 'Total number of rows: {}\t'.format(row_count)
    # print(message)
    successful_rows = 0
    failed_rows = 0

    # TODO: make this less hacky/kludgy and improve error handling + reporting
    if 'latest_export.csv' in csv_file:
        with open(csv_file, 'r') as file:
            reader = csv.DictReader(file)
            for row_num, row in enumerate(reader):
                row_as_dict = dict(row)
                now = str(timezone.now())
                # we never want to use the old related user id bc a new one needs to be made
                row_as_dict.pop('related_user')
                # adjust the following as needed before import
                if row_as_dict['created'] == '':
                    row_as_dict['created'] = now
                if row_as_dict['updated'] == '':
                    row_as_dict['updated'] = now
                if row_as_dict['timezone'] == '':
                    row_as_dict.pop('timezone')
                if row_as_dict['rating'] == '':
                    row_as_dict.pop('rating')
                if row_as_dict['rating_avg'] == '':
                    row_as_dict.pop('rating_avg')
                try:
                    create_person(row_num, failed_rows, row_as_dict)
                    successful_rows += 1
                except:
                    email_address = row_as_dict['email_address']
                    message = f'Failed to create a person for {email_address}. \nException: {str(sys.exc_info())}'
                    failed_rows += 1
                    print(message)
    else:
        with open(csv_file) as file:
            csv_reader = csv.DictReader(file)
            ## loops thru the rows
            for row_num, row in enumerate(csv_reader):
                ## special fields
                status = 'added_by_admin'
                email_address = row['email_address']
                try:
                    timezone_value = int(row['timezone'])
                except ValueError as e:
                    message = 'Error converting timezone to integer: {}'.format(e)
                    print(message)
                    timezone_value = None
                import pdb; pdb.set_trace()
                ## map fields from csv to Person model
                csv_to_model_dict = {
                    'role': row['role'],
                    'pronouns': row['pronouns'],
                    'first_name': row['first_name'],
                    'last_name': row['last_name'],
                    'type_of_expert': row['type_of_expert'],
                    'expertise': row['expertise'], ## m2m field
                    'title': row['title'],
                    'organization': row['organization'], ## m2m field
                    'city': row['city'],
                    'state': row['state'],
                    'country': row['country'],
                    'phone_number_primary': row['phone_number_primary'],
                    'phone_number_secondary': row['phone_number_secondary'],
                    'twitter': row['twitter'],
                    'notes': row['notes'],
                    'website': row['website'],
                    'prefix': row['prefix'],
                    'middle_name': row['middle_name'],
                    'language': row['language'], ## m2mfield
                    'approved_by_admin': False,
                    'approved_by_user': False,
                    'entry_method': 'import',
                    'entry_type': 'automated',
                    'email_address': email_address,
                    'status': status,
                    'timezone': timezone_value,
                    'skype': row['skype'],
                    'media_audio': row['media_audio'],
                    'media_text': row['media_text'],
                    'media_video': row['media_video'],
                }
                try:
                    create_person(row_num, failed_rows, csv_to_model_dict)
                    successful_rows += 1
                except:
                    pass
        # message = '\nThe following rows failed: \n\n {}'.format(failed_rows)
        # print(message)

    ## end
    end_time = datetime.now()
    end_message = '\nFinished import:\t {} \n'.format(end_time)
    import_length = end_time - start_time
    message = end_message
    print(message)
    message = 'Import length:\t\t {} \n'.format(import_length)
    print(message)

    message = 'Imported {} rows'.format(successful_rows)
    print(message)
    message = '{} rows failed'.format(failed_rows)
    print(message)


class Command(BaseCommand):
    help = 'Import sources from a csv file.'

    def add_arguments(self, parser):
        ## required
        parser.add_argument('file', 
            help='Specify the CSV file.'
        )

    def handle(self, *args, **options):
        ## unpack args
        csv_file = options['file']

        ## call the function
        import_csv(csv_file)

