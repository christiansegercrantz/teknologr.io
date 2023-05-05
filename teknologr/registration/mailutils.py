from django.core.mail import send_mail
from getenv import env


def mailApplicantSubmission(context, sender=env('EMAIL_APPLICANT_SENDER')):
    name = context['name']
    receiver = context['email']

    subject = 'Tack för din medlemsansökan till Teknologföreningen!'
    message = f'''Hej {name},

    Tack för din medlemsansökan till Teknologföreningen!

    För att bli en fullständig medlem så är nästa steg att delta i ett Nationsmöte (Namö).
    Detta informeras mera senare.

    Vid frågor eller ifall du inte ansökt om medlemskap, kontakta {sender}

    Detta är ett automatiskt meddelande, du behöver inte svara på det.
    '''

    return send_mail(
        subject,
        message,
        sender,
        [receiver],
        fail_silently=False)
