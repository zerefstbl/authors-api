from django.core.mail import send_mail

from django.template.loader import render_to_string

import os

from datetime import datetime

from .email_messages import new_account_message_email, new_follower_message_email


def send_email_on_create_account(user):
    assunto = 'Bem vindo(a) ao nosso serviço!!'

    message = new_account_message_email(user)

    html = render_to_string('email_new_user.html', context={'username': user.first_name})

    send_mail(
        fail_silently=False,
        message=message,
        subject=assunto,
        from_email=os.environ['EMAIL_ADRESS'],
        recipient_list=[user.email],
        html_message=html,
    )


def send_email_on_follow_account(user_followed, user_following):
    print(os.environ)

    assunto = 'Novo seguidor em seu perfil'

    message = new_follower_message_email(user_followed, user_following)

    context = {
        'user_followed': user_followed,
        'user_following': user_following,
        'date': datetime.now().strftime('%d/%m/%Y %H:%M'),
    }

    html = render_to_string('email_a_new_follower.html', context)

    send_mail(
        fail_silently=False,
        message=message,
        subject=assunto,
        from_email=os.environ['EMAIL_ADRESS'],
        recipient_list=[user_followed.email, 'duduoli11@hotmail.com'],
        html_message=html,
    )
