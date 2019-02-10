from django.core.management.base import BaseCommand, CommandError
from django.core.management import call_command
from django.contrib.auth.models import User, Group
from sources.models import Person
from sourcelist.settings import TEST_ENV
from datetime import datetime
import sys
import csv


# def export_csv():
def export_csv(csv_path):    
    ## start
    start_time = datetime.now()
    start_message = f'\nStarted export:\t {start_time}\n'
    message = start_message
    print(message)

    # get the data to export
    all_people = Person.objects.all()
    export_count = all_people.count()
    message = f'We will be exporting {export_count} records.\n'
    print(message)

    ## TO-DO: add ability to override via an argument
    export_filename = 'latest_export.csv'

    ## write csv
    with open(export_filename, 'w') as csvfile:
        csv_writer = csv.writer(csvfile)

        # header row prep
        model_fields = Person._meta.fields
        header_row = ''
        for field in model_fields:
            # construct the 
            header_row += f'{field},'
        # write the header row
        csv_writer.writerow(header_row)

        # go thru all the people
        for person in all_people:
            # construct the data row
            data_row += getattr(obj, field.name) + ","
            # add the row
            csv_writer.writerow(data_row)

    ## end
    end_time = datetime.now()
    end_message = f'\nFinished export:\t {end_time} \n'
    export_length = end_time - start_time
    message = end_message
    print(message)
    message = f'Export length:\t\t {export_length} \n'
    print(message)

    # get row count of the finished csv
    with open(export_filename, 'r') as finished_file:
        reader = csv.reader(finished_file, delimiter = ',')
        data = list(reader)
        row_count = len(data)

    # check if the numbers match
    if row_count == export_count:
        note = 'SUCCESS'
    else:
        note = 'INCOMPLETE'

    # let us know if numbers match
    message = f'{note}: Created {row_count} of {export_count} records'
    print(message)
    # message = '{} rows failed'.format(failed_rows)
    # print(message)


class Command(BaseCommand):
    help = 'Export all sources to a csv file.'

    # def add_arguments(self, parser):
    #     ## required
    #     parser.add_argument('file', 
    #         help='Specify the CSV file.'
    #     )

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
        # csv_path = options['file']

        ## call the function
        # export_csv()
        export_csv(csv_path)

