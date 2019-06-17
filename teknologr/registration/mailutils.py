from django.core.mail import send_mail


# TODO: check whether this should be sent from Phuxivator
def mailApplicantSubmission(context, sender='phuxivator@tf.fi'):
    name = context['name']
    receiver = context['email']

    subject = 'Tack för din medlemsansökan till Teknologföreningen!'
    message = '''Hej {name},

    Tack för din medlemsansökan till Teknologföreningen!

    För att bli en fullständig medlem så är nästa steg att delta i ett Nationsmöte (Namö).
    Detta informeras mera senare.

    Vid frågor eller ifall du inte ansökt om medlemskap, kontakt {sender}

    Detta är ett automatiskt meddelande, du behöver inte svara på det.
    '''.format(name=name, sender=sender)

    return send_mail(
        subject,
        message,
        sender,
        [receiver],
        fail_silently=False)
