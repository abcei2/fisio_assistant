from django.db import models
from django.contrib.auth.models import AbstractUser

from core.model_utils import BaseModel  
from datetime import timedelta, datetime

class Entity(BaseModel):
    legal_id = models.CharField(max_length=64, unique=True)
    name = models.CharField(max_length=128, unique=True, verbose_name="Nombre de entidad")
  
class User(AbstractUser, BaseModel):
    legal_id = models.CharField(max_length=64, unique=True)
    whatsapp_number = models.CharField(max_length=32, unique=True)    
    notified = models.BooleanField(default=False, verbose_name="El usuario ha sido notificado")
    authorized = models.BooleanField(default=False, verbose_name="Se recibe confirmación para mensajería libre/acepta términos")
    first_join = models.BooleanField(default=True, verbose_name="El usuario ha autorizado recibir mensajes")

    authorization_time = models.DateTimeField(auto_now_add=False, verbose_name="Tiempo en que el usuario autoriza recibir mensajes", default = datetime.now )    

    def free_way_messages(self):
        print(self.authorization_time, self.authorization_time > timedelta(days = 1), self.authorized ,self.notified)
        if (self.authorized or self.notified ) and self.authorization_time > timedelta(days = 1):
            self.authorized = False
            self.notified = False

    

class UserEntity(BaseModel):
    entity = models.ForeignKey(Entity, on_delete=models.CASCADE, verbose_name="Entidad")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Entidad")

    
