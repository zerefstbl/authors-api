from inspect import cleandoc

from datetime import datetime


def new_account_message_email(user):
    return cleandoc(f'''
      Olá {user.first_name} e seja bem-vindo(a) ao nosso serviço!

      Agradecemos por se cadastrar em nossa plataforma e estamos muito felizes em tê-lo(a) conosco. Esperamos que nossa plataforma atenda todas as suas necessidades e expectativas, e estamos à disposição para ajudá-lo(a) no que for preciso.

      Atenciosamente,
      Equipe do Serviço.
    ''')


def new_follower_message_email(user_followed, user_following):
    return cleandoc(f'''
      Olá { user_followed.username },

      Você tem um novo seguidor em seu perfil. É ótimo ver que outras pessoas estão interessadas em seu conteúdo!

      Aqui estão as informações do perfil do seu novo seguidor:
      Nome: {user_following.first_name}
      E-mail: {user_following.email}
      Data de registro: {datetime.now().strftime('%d/%m/%Y %H:%M')}

      Se você quiser verificar o perfil do seu novo seguidor, faça login em nosso site em e visite a seção "Seguidores" em seu perfil.

      Obrigado por usar nosso site!

      Atenciosamente,
      A equipe do Api do DUDU
    ''')
