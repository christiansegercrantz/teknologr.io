from django.core.management.base import BaseCommand, CommandError
from members.models import Member
from os.path import isfile
import csv


class Command(BaseCommand):
    help = 'Cross-reference emails found in the register with input list of emails'

    def add_arguments(self, parser):
        parser.add_argument('email_file', nargs=1, type=str)
        parser.add_argument('--removed-file', nargs='?', type=str, help='Name removed emails file')
        parser.add_argument(
            '--output-file',
            nargs='?',
            type=str,
            help='Name output file',
            default='found_emails.csv'
        )

    def handle(self, *args, **options):
        email_file = options['email_file'][0]
        if not isfile(email_file):
            raise CommandError('Could not find input file: {}'.format(email_file))

        def to_lower(emails): return [email.lower() for email in emails]

        def in_emails(email, emails): return email.lower() in emails

        input_emails = [
            arr[0]
            for arr in csv.reader(email_file)
        ]

        found_emails = [
            member.email
            for member in filter(
                lambda member: in_emails(member.email, to_lower(input_emails)),
                Member.objects.all()
            )
        ]

        email_intersection = list(filter(
            lambda email: not in_emails(email, to_lower(found_emails)),
            input_emails
        ))

        output_file = options['output_file']
        with open(output_file, 'w+') as fp:
            fp.write('\n'.join(found_emails))

        removed_emails_file = options['removed_file']
        if removed_emails_file:
            with open(removed_emails_file, 'w+') as fp:
                fp.write('\n'.join(email_intersection))
            self.stdout.write(self.style.SUCCESS('Saved all removed emails to {}'.format(removed_emails_file)))

        self.stdout.write(self.style.SUCCESS('Saved all found emails to {}'.format(output_file)))
