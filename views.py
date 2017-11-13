__author__ = 'irenebreck'

import pymongo
import sys
import os
import json

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

from pyramid.view import view_config
@view_config(route_name='UserProfile')
def UserProfileFormView(request):
   here    = os.path.dirname(__file__)
   profile = os.path.join(here, 'static','UserProfile.html')
   return (FileResponse(profile))

@view_config(route_name='attendEvent')
def getAttendance(request):
   param         = request.params
   event_choice  = param.get('event_choice')

   all_leads = col.find({'events':event_choice})
   return(json.dump(list(all_leads)))


@view_config(route_name='SubmitUserProfile')
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

       send_mail(request)
       return Response('ok %(name)s!' % request.matchdict)


def send_mail(request):

    mailer = Mailer( host='smtp.gmail.com',
                     port=587, #???
                     username='celiapan.noreply@gmail.com',
                     password='1234test',
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

    here = os.path.dirname(__file__)
    att1 = os.path.join(here, 'static','velur1.pdf')
    attachment = Attachment(att1, "image/jpg",
                        open(att1, "rb"))

    message.attach(attachment)

    here = os.path.dirname(__file__)
    att2 = os.path.join(here, 'static','velur2.pdf')
    attachment = Attachment(att2, "image/jpg",
                        open(att2, "rb"))

    message.attach(attachment)

   # mailer.send_immediately(message, fail_silently=False)
    mailer.send(message)
    return Response(email)


def view_root(context, request):
    return {'items':list(context), 'project':'pyramidapp'}

def view_model(context, request):
    return {'item':context, 'project':'pyramidapp'}
