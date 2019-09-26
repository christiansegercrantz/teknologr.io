from django.core.management.base import BaseCommand, CommandError
from members.models import Member
from os.path import isfile
import csv


class Command(BaseCommand):
    help = 'Get a list of student ids based on input file of emails'

    def add_arguments(self, parser):
        parser.add_argument('email_file', nargs=1, type=str)
        parser.add_argument('--output-file', nargs='?', type=str, help='Name output file', default='found_ids.csv')

    def handle(self, *args, **options):
        email_file = options['email_file'][0]
        if not isfile(email_file):
            raise CommandError('Could not find input file: {}'.format(email_file))

        with open(email_file, 'r') as fp:
            reader = csv.reader(fp)
            emails = [email[0].lower() for email in reader]

        student_ids = [
            member.student_id
            for member in filter(
                lambda member: member.email.lower() in emails,
                Member.objects.all()
            )
        ]

        output_file = options['output_file']
        with open(output_file, 'w+') as fp:
            fp.write('\n'.join(student_ids))

        self.stdout.write(self.style.SUCCESS('Saved all found student ids to {}'.format(output_file)))
