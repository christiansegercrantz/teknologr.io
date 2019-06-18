from django.core.mail import send_mail


def mailNewPassword(member, password, sender="infochef@tf.fi"):

    subject = 'Ditt nya TF-lösenord'

    message = '''Hej,

    Här är ditt nya TF-lösenord:

    %s

    Vänligen logga in på TF:s hemsida och byt lösenordet så snabbt som möjligt:
    https://medlem.teknologforeningen.fi/index.php/aendra-loesenord

    Vid frågor eller ifall du inte begärt detta, kontakta %s

    Detta är ett automatiskt meddelande, du behöver inte svara på det.
    ''' % (password, sender)

    receiver = member.email

    return send_mail(
        subject,
        message,
        sender,
        [receiver],
        fail_silently=False)
