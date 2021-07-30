from django.shortcuts import render
from twilio.twiml.messaging_response import MessagingResponse

import requests
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from assistant.models import VirtualSession


# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure
account_sid = ""
auth_token = ""
MAXIMUM_MESSAGE_LENGTH = 1600 

# 1). Sacar número del que envia.
# 2). Intentar enviar el video

@csrf_exempt 
def bot(request):
    
    incoming_msg = request.POST.get('Body').lower()
    from_who = request.POST.get('From').lower()
    started_sessions = [obj for obj in VirtualSession.objects.all() if obj.patient.whatsapp_number == from_who[12:] and obj.already_started and not obj.session_done]
    resp = MessagingResponse()
    msg = resp.message()
    body = ""
    for session in started_sessions:
        body += f"*Bienvenido {session.patient.first_name} a su sesión virtual {session.start_time}*\n"
        body += f"*Con el especialista:*{session.specialist.first_name}\n"
        body += f"Acontinuación las indicaciones del especiaista\n"
        body += f"{session.description_message}\n"
        for virtualsessionvideo in session.virtualsessionvideo_set.all():
            print(virtualsessionvideo)
            body += f"{virtualsessionvideo.video.source_link}\n" 
        
        session.user_notified = True   
        session.user_authorized = True   
        session.session_done = True   
        session.session_status_message =  "Se envía mensaje al usuario."
        session.save()
        
        session.patient.first_join = True     
        session.patient.authorized = True   
        session.patient.notified = True  
        session.patient.save()
    msg.body(body)
    print(body)
    
    return HttpResponse(str(resp))
