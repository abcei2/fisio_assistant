from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now

from core.model_utils import BaseModel  
from django.utils import timezone

class Entity(BaseModel):
    legal_id = models.CharField(max_length=64, unique=True)
    name = models.CharField(max_length=128, unique=True, verbose_name="Nombre de entidad")
  
class User(AbstractUser, BaseModel):
    legal_id = models.CharField(max_length=64, unique=True)
    whatsapp_number = models.CharField(max_length=32, unique=True)    
    authorized = models.BooleanField(default=False, verbose_name="Se recibe confirmación para mensajería libre/acepta términos")
    first_join = models.BooleanField(default=True, verbose_name="El usuario ha autorizado recibir mensajes")

    authorization_time = models.DateTimeField(auto_now_add=False, verbose_name="Tiempo en que el usuario autoriza recibir mensajes", default = now )    

    def free_way_messages(self):
        if  timezone.now() > self.authorization_time+ timezone.timedelta(days=1):
            self.authorized = False
            self.save()
            return False
        else:
            return True

            
    def __str__(self):
        return f"{self.first_name} {self.last_name}"


    

class UserEntity(BaseModel):
    entity = models.ForeignKey(Entity, on_delete=models.CASCADE, verbose_name="Entidad")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Entidad")

    
