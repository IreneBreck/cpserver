import pymongo
import sys
import os

from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.response import Response
from pyramid.response import FileResponse

from pyramid_mailer.mailer import Mailer
from pyramid_mailer.message import Message
from pyramid_mailer.message import Attachment


# connnecto to the db on standard port
connection = pymongo.MongoClient("mongodb://admin:manager@ds043378.mongolab.com:43378/velur")

#connection = pymongo.MongoClient("mongodb://localhost")
db = connection.velur                # attach to db
col = db.userprofile                 # specify the colllection

#col = connection.userprofile

def hello_world(request):
    return Response('Hello %(name)s!' % request.matchdict)

def UserProfileFormView(request):
       return (FileResponse('UserProfile.html'))

def SubmitUserProfileView(request):

       params = request.params


       firstname = request.params['firstname']
       lastname  = request.params['lastname']
       password  = request.params['password']
       email     = request.params['email']
       phonenumber = request.params['phonenumber']

# need to make sure if key/data exist. None (null) will be returned if not existed

       agent_q = params.get('agent_q')
       seminar_q = params.get('seminar_q')
       land_q    = params.get('land_q')
       when      = params.get('when')
       where     = params.get('where')
       events    = params.getall("event_choice")

       col.insert({'fname': firstname,
                   'lname': lastname,
                   'password': password,
                   'email':email,
                   'phonenumber': phonenumber,
                   'events': events,
                   'agent_q': agent_q,
                   'seminar_q': seminar_q,
                   'land_q' : land_q,
                   'when'   : when,
                   'where'  : where
        })


      #send_mail(request)
       return Response('ok %(name)s!' % request.matchdict)


def send_mail(request):

    mailer = Mailer( host='smtp.gmail.com',
                     port=587, #???
                     username='your@emal.com',
                     password='password',
                     tls=True)

    if request.params.get('email') is not None:
        email = request.params['email']
    else:
        email = "the email does not exist"

    send_topic = 'Welcome to join us for the seminar'
    send_er = 'irenebreck@gmail.com'
    send_to = [email]
    send_this = "Thank you for signing up at our website..."

    message = Message( subject = send_topic,
                       sender = send_er,
                       recipients = send_to,
                       body = send_this )

    attachment = Attachment("velur1.pdf", "image/jpg",
                        open("velur1.pdf", "rb"))

    message.attach(attachment)

    attachment = Attachment("velur2.pdf", "image/jpg",
                        open("velur2.pdf", "rb"))

    message.attach(attachment)

   # mailer.send_immediately(message, fail_silently=False)
    mailer.send(message)
    return Response(email)


if __name__ == '__main__':
    config = Configurator()

    config.add_route('hello', '/hello/{name}')
    config.add_view(hello_world, route_name='hello')

    config.add_route('UserProfile', '/UserProfile/{name}')
    config.add_view(UserProfileFormView, route_name='UserProfile')

    config.add_route('SubmitUserProfile', '/SubmitUserProfile/{name}')
    config.add_view(SubmitUserProfileView, route_name='SubmitUserProfile')

    app = config.make_wsgi_app()
    server = make_server('0.0.0.0', 8080, app)
    server.serve_forever()
