from django.shortcuts import render
from twilio.twiml.messaging_response import MessagingResponse

import requests
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from assistant.models import VirtualSession
from django.utils import timezone
import unidecode


# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure
account_sid = ""
auth_token = ""
MAXIMUM_MESSAGE_LENGTH = 1600 
"""Your appointment is coming up on {{1}} at {{2}}"""
# 1). Sacar número del que envia.
# 2). Intentar enviar el video

@csrf_exempt 
def bot(request):
    incoming_msg = unidecode.unidecode(request.POST.get('Body').lower())
    print(incoming_msg)
    from_who = request.POST.get('From').lower()
    ammount_words = len(incoming_msg.split())
    words = incoming_msg.split()

    body = "" 
    resp = MessagingResponse()
    msg = resp.message()
    
    started_sessions = [obj for obj in VirtualSession.objects.all() if obj.patient.whatsapp_number == from_who[12:] and obj.already_started and not obj.session_done]
    if len(started_sessions) > 0:
        if ammount_words==1: 
            if 'si' in words:   

                for session in started_sessions:
                    body += f"*¡Bienvenido/a {session.patient.first_name} {session.patient.last_name} a su sesión virtual de hoy!* \n" #
                    body += f"Con el especialista *{session.specialist.first_name} {session.specialist.last_name}*\n\n"

                    if session.description_message:
                        body += f"A continuación las indicaciones del especialista\n"
                        body += f"{session.description_message}\n\n"
                    counter=1
                    for virtualsessionvideo in session.virtualsessionvideo_set.all():
                        body += f"{counter}. {virtualsessionvideo.video.title}\n{virtualsessionvideo.video.source_link}\n\n" 
                        counter=counter+1
                    
                    session.user_notified = True   
                    session.user_authorized = True   
                    session.session_done = True   
                    session.session_status_message =  "Se envía mensaje al usuario. Sesión finalizada con éxito."
                    session.save()
                    
                    session.patient.first_join = True     
                    session.patient.authorized = True  
                    session.patient.authorization_time = timezone.now()
                    session.patient.save()
            elif 'no' in words:
                
                for session in started_sessions:
                    session.user_notified = True   
                    session.user_authorized = False   
                    session.session_done = True   
                    session.session_status_message =  "El usuario no acepta continuar con la sesión"
                    session.save()
                    session.patient.authorized = False              
                    session.patient.save()
                body += "Muchas gracias por su tiempo, porfavor indiquenos a continuación las inquietudes que tenga."
        else:
            body += "Porfavor indique claramente '*sí*' desea continuar con la sesión o '*no*' quiere continuar."
    msg.body(body)
    print(body)
    if body:
        return HttpResponse(str(resp))
    else:
        return HttpResponse("")
