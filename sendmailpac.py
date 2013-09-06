
import os

from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.response import Response
from pyramid.response import FileResponse

from pyramid_mailer.mailer import Mailer
from pyramid_mailer.message import Message

def send_mail(request):
    mailer = Mailer( host='smtp.gmail.com',
                     port=587, #???
                     username='zaycoder@gmail.com',
                     password='ZC783921',
                     tls=True)



    if request.params.get('email') is not None:
        email = request.params['email']
    else:
        email = "the email does not exist"
    if request.params.get('message') is not None:
        note = request.params['message']
    else:
        note = "should t'his 'w''o'rk?"

    send_topic = 'Welcome'
    send_er = 'zaycoder@gmail.com'
    send_to = ['isaiahpan@gmail.com']
    send_this = note

    message = Message( subject = send_topic,
                       sender = send_er,
                       recipients = send_to,
                       body = send_this )
    mailer.send_immediately(message, fail_silently=False)
    return Response(email)
