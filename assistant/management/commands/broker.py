
from django.core.management.base import BaseCommand
from assistant.models import VirtualSession
from ui.models import User
import time

from twilio.rest import Client

ERROR_CODES={
    "63015":"Phone must join on sandbox"
}

# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure
account_sid = "AC0d15ec2e3c206afdff8251c3b073945d"
auth_token = "f7f05021caa1806f8724241d4a5d77ca"
client = Client(account_sid, auth_token)
# template_1 = 'Fisio-Online'
# template_2 = '0000'
# message = client.messages.create(
#     from_='whatsapp:+14155238886',
#     body=f'Your {template_1} code is {template_2}',
#     to='whatsapp:+573117064404'
# )

def send_message(body, recipient, sender="4155238886",rec_county_id="+57",sender_county_id="+1"):    
    message = client.messages.create(
        from_=f'whatsapp:{sender_county_id}{sender}',
        body=body,
        to=f'whatsapp:{rec_county_id}{recipient}'
    )
    return message
    
def send_notification(send_message_timer,send_message_period):
    notifications = [obj for obj in VirtualSession.objects.all() if obj.patient.first_join and obj.already_started and not obj.user_notificated ]
    num_noti_to_send = len(notifications)
    while num_noti_to_send>0:
        if time.time()-send_message_timer > send_message_period:
            notification = notifications[num_noti_to_send-1]
            whatsapp_number = notification.patient.whatsapp_number
            if notification.patient.first_join:                      
                template_1 = 'Fisio-Online'
                template_2 = '0000'
                body = f'Your {template_1} code is {template_2}'
                message=send_message(body, whatsapp_number)
                    
                while message.status == "queued":                            
                    message = client.messages(message.sid).fetch()  

                if str(message.error_code) in ERROR_CODES.keys():         
                    notification.patient.first_join = False                    
                    notification.patient.save()                       
                    print(ERROR_CODES[str(message.error_code)])
                else:
                    print("noti send")
                num_noti_to_send = num_noti_to_send - 1 
                send_message_timer = time.time()
    if len(notifications)==0:
        print("Seems that all notification were send")
    
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
