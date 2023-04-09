import os
from django.core.mail import send_mail


def sendEmailSES(subject, message, recipient):
    send_mail(
        from_email=os.getenv('SENDER_EMAIL'),
        recipient_list=recipient,
        subject=subject,
        message=message,
        html_message=message,
        fail_silently=True
    )
