from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now

from core.model_utils import BaseModel  
from django.utils import timezone


MAX_NO_SESSION_MESSAGES=10
TIME_TO_UNBLOCK=1
MAX_SECONDS_BETWEEN_MESSAGES_RESET=5
class Entity(BaseModel):
    legal_id = models.CharField(max_length=64, unique=True)
    name = models.CharField(max_length=128, unique=True, verbose_name="Nombre de entidad")
  
class User(AbstractUser, BaseModel):
    legal_id = models.CharField(max_length=64, unique=True)
    whatsapp_number = models.CharField(max_length=32, unique=True)    
    authorized = models.BooleanField(default=False, verbose_name="Se recibe confirmación para mensajería libre/acepta términos")
    first_join = models.BooleanField(default=True, verbose_name="El usuario ha autorizado recibir mensajes (firma documento)")
    
    
    no_session_message_count = models.IntegerField(default=0, verbose_name="Cuenta la cantidad de mensajes que se responde al usuario")
    last_time_write = models.DateTimeField( verbose_name="Ultima fecha en la que el usuario fue bloqueado", null=True)
    
    authorization_time = models.DateTimeField(verbose_name="Tiempo en que el usuario autoriza recibir mensajes", default = now )    

    def free_way_messages(self):
        if  timezone.now() > self.authorization_time+ timezone.timedelta(days=1):
            self.authorized = False
            self.save()
            return False
        else:
            return True

    
    def send_no_session_message(self):
        '''
            This functions aims to control spam by blocking an user 
            who sents MAX_NO_SESSION_MESSAGES messages at rate
            faster than MAX_NO_SESSION_MESSAGES/MAX_SECONDS_BETWEEN_MESSAGES_RESET
            (message/seconds) is blocked for TIME_TO_UNBLOCK.           
           
        '''
        if  self.no_session_message_count < MAX_NO_SESSION_MESSAGES:
                        
            if timezone.now()<self.last_time_write+timezone.timedelta(seconds=MAX_SECONDS_BETWEEN_MESSAGES_RESET):
                self.no_session_message_count= self.no_session_message_count +  1
            else:
                self.no_session_message_count = 0
                
            self.last_time_write = timezone.now()         
            self.save()
            
            return True       
        else:
            if timezone.now()<self.last_time_write+timezone.timedelta(minutes=TIME_TO_UNBLOCK):
                return False
            else:                    
                self.no_session_message_count = 0
                self.save()
                return True

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


    

class UserEntity(BaseModel):
    entity = models.ForeignKey(Entity, on_delete=models.CASCADE, verbose_name="Entidad")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Entidad")

    
