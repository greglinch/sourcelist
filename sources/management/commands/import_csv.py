from django.core.management.base import BaseCommand, CommandError
from django.core.management import call_command
from django.contrib.auth.models import User, Group
from sources.models import Person
from sourcelist.settings import TEST_ENV
from datetime import datetime
import sys
import csv


# def import_csv():
def import_csv(csv_path):    
    ## start
    start_time = datetime.now()
    start_message = '\nStarted import:\t {}\n'.format(start_time)
    message = start_message
    print(message)

    ## read csv
    with open(csv_path) as csv_file:
        csv_reader = csv.DictReader(csv_file)
        # row_count = sum(1 for row in csv_reader)
        # message = 'Number of rows: {}\t'.format(row_count)
        # print(message)
        counter = 0
        failed_rows = 0
        # import pdb; pdb.set_trace()
        ## loops thru the rows
        for row in csv_reader:
            counter += 1
            ## special fields
            status = 'added_by_admin'
            email_address = row['email_address']
            if isinstance(row['timezone'], int):
                timezone = row['timezone']
            else:
                timezone = None
            ## map fields from csv to Person model
            csv_to_model = {
                'role': row['role'],
                'first_name': row['first_name'],
                'last_name': row['last_name'],
                'type_of_expert': row['type_of_expert'],
                'expertise': row['expertise'], ## m2m field
                'title': row['title'],
                'organization': row['organization'], ## m2m field
                'city': row['city'],
                'state': row['state'],
                'country': row['country'],
                'phone_number_primary': row['phone_primary'],
                'phone_number_secondary': row['phone_secondary'],
                'twitter': row['twitter'],
                'notes': row['notes'],
                # 'website': row['website'],
                'prefix': row['prefix'], 
                # 'middle_name': '',
                # 'language': 'English', ## m2mfield
                'entry_type': 'automated',
                'email_address': email_address,
                'status': status,
                'timezone': timezone,
            }
            ## create the source Person
            # try:
            try:
                exists = Person.objects.get(email_address=email_address)
                counter -= 1
            except:
                try:
                    obj, created = Person.objects.update_or_create(**csv_to_model)
                except Exception as e:
                    failed_rows += 1
                    message = 'Row {}: {}\n'.format(counter, e)
                    print(message)
            # except:
                # failed_rows.append(counter)
            # try:
            #     obj, created = Person.objects.create(**csv_to_model)
            # except:
            #     message = 'Create person' + str(sys.exc_info())
            #     print(message)
            ## set the related user and email them
            # try:
            #     call_command('set_related_user', email_address)
            # except:
            #     message = 'Set related user: ' + str(sys.exc_info())
            #     print(message)
            # if not TEST_ENV:
                # try:
                #     call_command('email_user', email_address, status)
                # except:
                #     message = 'Email user:' + str(sys.exc_info())
                #     print(message)
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

    message = 'Imported {} rows'.format(counter)
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

        ## optional
        # parser.add_argument('-f' '--file',
        #     action='store_true',
        #     # type=str,
        #     dest='file',
        #     default=False,
        #     help='Specify the file'
        # )

    def handle(self, *args, **options):
        ## unpack args
        csv_path = options['file']

        ## call the function
        # import_csv()
        import_csv(csv_path)

