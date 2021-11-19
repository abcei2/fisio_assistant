from django.shortcuts import render
from twilio.twiml.messaging_response import MessagingResponse

import requests
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from assistant.models import VirtualSession, VirtualSessionMessages
from ui.models import User
from django.utils import timezone
import unidecode


# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure
account_sid = ""
auth_token = ""
MAXIMUM_MESSAGE_LENGTH = 1600 
# 1). Sacar número del que envia.
# 2). Intentar enviar el video

def save_commentary(session,message):       
    commentary=VirtualSessionMessages()
    commentary.session = session
    commentary.message = message
    commentary.save()

def user_confirm_session(started_sessions,incoming_msg):
    '''
        Confirm each session already started for an user 
        because there aren't in theory more than one session at time,
        and continue to the commentary section.
    '''
    body=""
    for session in started_sessions:
        body += f"*¡Bienvenido/a {session.patient.first_name} {session.patient.last_name} a su sesión virtual de hoy!* \n" #
        body += f"Con el especialista *{session.specialist.first_name}* *{session.specialist.last_name}*\n\n"

        if session.description_message:
            body += f"A continuación las indicaciones del especialista\n"
            body += f"{session.description_message}\n\n"
        counter=1
        for virtualsessionvideo in session.virtualsessionvideo_set.all():
            body += f"{counter}. {virtualsessionvideo.video.title}\n{virtualsessionvideo.video.source_link}\n\n" 
            counter=counter+1
        body +=f"\n Si tiene algun comentario sobre la sesión porfavor escribalo acontinuación."
        session.user_notified = True   
        session.user_authorized = True   
        session.commentary_messages_section = True   
        session.session_status_message =  "Se envía mensaje al usuario. Sesión finalizada con éxito."
        session.save()
  
        session.patient.first_join = True     
        session.patient.authorized = True  
        session.patient.authorization_time = timezone.now()
        session.patient.save()

        save_commentary(session,incoming_msg)
    return body


def user_decline_session(started_sessions, incoming_msg):
    '''
        Decline each session already started for an user 
        because there aren't in theory more than one session at time,
        and continue to the commentary section.
    '''
    body=""
    for session in started_sessions:
        session.user_notified = True   
        session.user_authorized = False   
        session.commentary_messages_section = True   
        session.session_status_message =  "El usuario no acepta continuar con la sesión"
        session.save()
        
        session.patient.authorized = False              
        session.patient.save()

        save_commentary(session,incoming_msg)
    body += "Muchas gracias por su tiempo, porfavor indiquenos a continuación las inquietudes que tenga."
    return body
    
def user_commentary_session(started_commentary_sessions, incoming_msg):
    '''
        Find each session that is waiting for user end session commentary
    '''
    body=""
    if len(started_commentary_sessions) > 0:
        print("saving commentary")
        if started_commentary_sessions:
            for commentary_session in started_commentary_sessions:                    
                save_commentary(commentary_session,incoming_msg)                
                commentary_session.session_done = True   
                commentary_session.session_status_message +=  "\nUser send commentary."
                commentary_session.save()                
        body +="Muchas gracias por su comentario, será tenido en cuenta para mejorar nuestro servicio."
    return body

def no_session_avaliable(started_sessions,started_commentary_sessions,user_writing):
    '''
        Send a default message to register user, do not send anything when number
        isn't register to an user.
    '''
    body=""
    if len(started_commentary_sessions) == 0 and len(started_sessions)== 0:    
        if user_writing.send_no_session_message():
            body = "Su sesión ha caducado o no tiene activa ninguna sesión en el momento, porfavor comuniquese con el especialista."

    return body

@csrf_exempt 
@require_http_methods([ "POST"])
def bot(request):
    incoming_msg = unidecode.unidecode(request.POST.get('Body').lower())
    print(incoming_msg)
    from_number = request.POST.get('From').lower()
    from_number =  from_number[12:]
    words = incoming_msg.split()

    try:
        user_writing=User.objects.get(whatsapp_number=from_number)       
    except DoesNotExist:
        print("No existe usuario registrado con este número. No se le responde.")
        return HttpResponse("")

    body = "" 
    resp = MessagingResponse()
    msg = resp.message()

    #FIRST ASK IF THERE ARE COMMENTRIES INCOMMING
    started_commentary_sessions = [
        obj for obj in VirtualSession.objects.all() 
        if obj.patient.whatsapp_number == from_number and obj.already_started
        and not obj.session_done and obj.commentary_messages_section
    ] 
    body += user_commentary_session(started_commentary_sessions, incoming_msg)
    
    started_sessions=[]
    for obj in VirtualSession.objects.all():

        if not obj.session_expired and \
            obj.patient.whatsapp_number == from_number and \
            obj.already_started and \
            not obj.session_done and \
            not obj.commentary_messages_section:

            started_sessions.append(obj)

    #THEN ASK  IF THERE ARE NO SESSIONS FOR USER
    body += no_session_avaliable(started_sessions,started_commentary_sessions,user_writing)

    if len(started_sessions) > 0:
        if 'si' in words or 'si, estoy listo' in incoming_msg:   
            body += user_confirm_session(started_sessions,incoming_msg)           
        elif 'no' in words or 'no, necesito ayuda' in incoming_msg:            
            body += user_decline_session(started_sessions,incoming_msg)            
        else:
            body += "Porfavor indique claramente '*sí*' desea continuar con la sesión o '*no*' quiere continuar."    
  
   
    msg.body(body)


    if body:
        return HttpResponse(str(resp))
    else:
        return HttpResponse("")
