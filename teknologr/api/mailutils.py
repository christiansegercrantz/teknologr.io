from django.core.mail import send_mail
from getenv import env


def mailNewPassword(member, password, sender=env('EMAIL_LDAP_SENDER')):

    subject = 'Ditt nya TF-lösenord'

    message = f'''Hej,

    Här är ditt nya TF-lösenord:

    {password}

    Vänligen logga in och byt lösenordet så snabbt som möjligt:
    https://id.tf.fi/realms/tf-medlemmar/account/#/security/signingin

    Vid frågor eller ifall du inte begärt detta, kontakta {sender}

    Detta är ett automatiskt meddelande, du behöver inte svara på det.
    '''

    receiver = member.email

    return send_mail(
        subject,
        message,
        sender,
        [receiver],
        fail_silently=False)


def mailNewAccount(member, password, sender=env('EMAIL_LDAP_SENDER')):

    subject = 'Ditt nya TF-konto'

    message = f'''Hej,

    Ett TF-konto har skapats åt dig med följande inloggningsuppgifter:

    Användarnamn: {member.username}
    Lösenord: {password}

    Vänligen logga in och byt lösenordet så snabbt som möjligt:
    https://id.tf.fi/realms/tf-medlemmar/account/#/security/signingin

    Vid frågor eller ifall du inte begärt detta, kontakta {sender}

    Detta är ett automatiskt meddelande, du behöver inte svara på det.
    '''

    receiver = member.email

    return send_mail(
        subject,
        message,
        sender,
        [receiver],
        fail_silently=False)
