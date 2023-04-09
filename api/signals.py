import os
from django.dispatch.dispatcher import receiver

from django_rest_passwordreset.signals import reset_password_token_created, post_password_reset
from api.aws_ses_email import sendEmailSES


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    """Función para enviar el email con el token de restablecimiento de contraseña

    Args:
        reset_password_token (Any): Contiene la información del usuario y el token
    """
    # render email text
    email_data = {
        "name": reset_password_token.user.name,
        "first_name": reset_password_token.user.first_name,
        "url":  "{}/{}".format(
                os.getenv('FRONT_URL')+'/password-reset',
                reset_password_token.key)
    }
    sendEmailSES(
        subject="Completa tu solicitud de restablecimiento de contraseña",
        message_data=email_data,
        recipient=[reset_password_token.user.email],
        template_id=os.getenv('RESET_PASSWORD_EMAIL_TEMPLATE_ID'),
    )


@receiver(post_password_reset)
def confirm_password_reset(sender, user, **kwargs):
    try:
        print('User password reset 🚀💥', user)
    except Exception as error:
        print('Error: 💥', error)
