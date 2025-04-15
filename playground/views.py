from  django.core.mail import  send_mail,EmailMessage, mail_admins,BadHeaderError
from templated_mail.mail import BaseEmailMessage
from django.shortcuts import render


def say_hello(request):
    try:
        message = BaseEmailMessage(
            template_name='email/hello.html',
            context={'name': 'Mosh'},

        )
        message.send(['irfan@gmail.com'])
        # message = EmailMessage('subject','message','info@irfan.com',['safi@gmail.com'])
        # message.attach_file('playground/static/images/pic.jpg')
        # message.send()
        # mail_admins('subject','message',html_message='message')
        # send_mail('subject','message','info@irfan.com',['safi@gmail.com'])
    except BadHeaderError:
        pass
    return render(request, 'hello.html', {'name': 'Mosh'})
