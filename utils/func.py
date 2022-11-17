from django.core.mail import send_mail

def send_email(to_email,subject,body):
    try:
        send_mail(
            subject,
            body,
            "emails@itsashw.in" ,
            [to_email],
            fail_silently=False,
        )
        return True
    except:
        return False
