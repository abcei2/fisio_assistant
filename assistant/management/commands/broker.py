
from django.core.management.base import BaseCommand
from assistant.models import VirtualSession
import time

from twilio.rest import Client

ERROR_CODES={
    "63015":"Phone must join on sandbox",
    
    "63016":"Failed to send freeform message because you are outside the allowed window. Please use a Template.",
      
}
# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure
account_sid = ""
auth_token = ""
client = Client(account_sid, auth_token)
# template_1 = 'Fisio-Online'
# template_2 = '0000'
# message = client.messages.create(
#     from_='whatsapp:+14155238886',
#     body=f'Your {template_1} code is {template_2}',
#     to='whatsapp:+573117064404'
# )

def session_without_errors(session, error_code):
    if error_code== "63015":  
        session.patient.first_join = False     
        session.patient.authorized = False   
        session.patient.notified = False                  
        session.patient.save()     
        session.user_notified = False   
        session.user_authorized = False   
        session.session_status_message =  ERROR_CODES["63015"]
        session.save()                 
        return False
    elif error_code == "63016":         
        session.patient.notified = False          
        session.patient.authorized = False     
        session.patient.save()    
        session.user_notified = False       
        session.user_authorized = False      
        session.session_status_message =  ERROR_CODES["63016"] 
        session.save()    
        return False 
    else:        
        return True

def send_message(body, recipient, sender="4155238886",rec_county_id="+57",sender_county_id="+1"):    
    message = client.messages.create(
        from_=f'whatsapp:{sender_county_id}{sender}',
        body=body,
        to=f'whatsapp:{rec_county_id}{recipient}'
    )
    return message
    
def send_notification(send_message_timer,send_message_period):

    sessions = [obj for obj in VirtualSession.objects.all() if obj.patient.first_join and obj.already_started and not obj.user_notified and not obj.user_authorized and not obj.session_done ]
    num_noti_to_send = len(sessions)
    while num_noti_to_send>0:

        if time.time()-send_message_timer > send_message_period:
            session = sessions[num_noti_to_send-1]
            if not session.patient.notified:
                whatsapp_number = session.patient.whatsapp_number
                if session.patient.first_join:                      
                    template_1 = 'Fisio-Online'
                    template_2 = '0000 please write something :v'
                    body = f'Your {template_1} code is {template_2}'
                    message=send_message(body, whatsapp_number)
                        
                    while message.status == "queued":                            
                        message = client.messages(message.sid).fetch()  
                    send_message_timer = time.time()

                    if session_without_errors(session, str(message.error_code)):      
                        session.user_notified = True          
                        session.session_status_message = "El usuario ha sido notificado"
                        session.save()     
                        session.patient.notified = True          
                        session.patient.save()   
                        
                        print("noti send")
            else:
                session.user_notified = True          
                session.save()     

            num_noti_to_send = num_noti_to_send - 1 
    if len(sessions)==0:
        print("Seems that all session were send")
    


class Command(BaseCommand):
    help = 'Displays current time'
    def handle(self, *args, **kwargs):
        
        query_session_timer = time.time()
        send_message_timer = time.time()
        query_sessions_period = 1 # Time to query virtual sessions in seconds
        send_message_period = 1 # Time to send any message in seconds
        while True:
            if time.time()-query_session_timer > query_sessions_period:
                
                send_notification(send_message_timer,send_message_period)
                query_session_timer = time.time()
