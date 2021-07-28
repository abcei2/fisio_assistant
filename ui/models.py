from django.db import models
from django.contrib.auth.models import AbstractUser

from core.model_utils import BaseModel  

class Entity(BaseModel):
    legal_id = models.CharField(max_length=64, unique=True)
    name = models.CharField(max_length=128, unique=True, verbose_name="Nombre de entidad")
  
class User(AbstractUser, BaseModel):
    legal_id = models.CharField(max_length=64, unique=True)
    whatsapp_number = models.CharField(max_length=32, unique=True)

class UserEntity(BaseModel):
    entity = models.ForeignKey(Entity, on_delete=models.CASCADE, verbose_name="Entidad")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Entidad")

    
