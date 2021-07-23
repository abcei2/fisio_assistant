from django.db import models
from django.contrib.auth.models import AbstractUser

from core.model_utils import BaseModel  

class Entity(AbstractUser, BaseModel):
    legal_id = models.CharField(max_length=64, unique=True)
    name = models.CharField(max_length=128, unique=True, verbose_name="Nombre de entidad")
  
class Specialist(AbstractUser, BaseModel):
    entity = models.ForeignKey(Entity, on_delete=models.CASCADE, verbose_name="Entidad")
    legal_id = models.CharField(max_length=64, unique=True,blank=True,null=True)
    name = models.CharField(max_length=128, verbose_name="Nombre de especialista")  

class Patient(AbstractUser, BaseModel):
    entity = models.ForeignKey(Entity, on_delete=models.CASCADE, verbose_name="Entidad")
    legal_id = models.CharField(max_length=64, unique=True)
    name = models.CharField(max_length=128, verbose_name="Nombre de paciente")
    whatsapp_number = models.CharField(max_length=32, unique=True)

