from email import message
from pyclbr import Class
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template

class Mail:
    @staticmethod
    def send_complete_order(order, user):
        subject = 'Tú pedido ha sido enviado'
        template = get_template('mails/complete.html')
        content = template.render({
            'user':user,
            'order':order,
        })
       
        message = EmailMultiAlternatives(
            subject,'Mensaje importante',
            settings.EMAIL_HOST_USER,
            [user.email]
        )

        message.attach_alternative(content, 'text/html')
        message.send()