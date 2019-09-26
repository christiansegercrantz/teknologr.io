from django.core.management.base import BaseCommand, CommandError
from members.models import Member
from os.path import isfile


class Command(BaseCommand):
    help = 'Get a list of emails based on an input file of student ids'

    def add_arguments(self, parser):
        parser.add_argument('id_file', nargs=1, type=str)
        parser.add_argument('--output-file', nargs='?', type=str, help='Name output file', default='found_emails.csv')

    def handle(self, *args, **options):
        id_file = options['id_file'][0]
        if not isfile(id_file):
            raise CommandError('Could not find input file: {}'.format(id_file))

        with open(id_file, 'r') as fp:
            ids = fp.readlines()

        filtered_members = Member.objects.filter(student_id__in=ids)

        output_file = options['output_file']
        with open(output_file, 'w+') as fp:
            for member in filtered_members:
                email = member.email
                if email:
                    fp.write('{}\n'.format(email))

        self.stdout.write(self.style.SUCCESS('Saved all found emails to {}'.format(output_file)))
