from django.core.mail import send_mail

from inspect import cleandoc


def send_email_on_create_account(user):
    assunto = 'Bem vindo(a) ao nosso serviço!!'

    message = cleandoc(f'''
      Olá {user.first_name} e seja bem-vindo(a) ao nosso serviço!

      Agradecemos por se cadastrar em nossa plataforma e estamos muito felizes em tê-lo(a) conosco. Esperamos que nossa plataforma atenda todas as suas necessidades e expectativas, e estamos à disposição para ajudá-lo(a) no que for preciso.

      Atenciosamente,
      Equipe do Serviço.
    ''')

    send_mail(
        fail_silently=False,
        message=message,
        subject=assunto,
        from_email='apidrfteste1@outlook.com',
        recipient_list=[user.email],
    )


# def send_email_on_follow_account(user):
#     assunto = 'Um novo usúario começou a seguir você!!'
