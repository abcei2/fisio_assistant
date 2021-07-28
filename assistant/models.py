from django.db import models
from ui.models import Entity, User
from core.model_utils import BaseModel  
# Create your models here.


class Videos(BaseModel):
    
    entity = models.ForeignKey(Entity, on_delete=models.CASCADE, verbose_name="Entidad")
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, verbose_name="Especialista", null=True)
    title = models.TextField(max_length=1024, verbose_name="Titulo")
    source_link = models.URLField(max_length=1024, verbose_name="Link del recurso")
    description = models.TextField(
        max_length=4096, blank=True, verbose_name="Descripción"
    )
    
# class VideosUser(BaseModel):
    
#     entity = models.ForeignKey(Entity, on_delete=models.CASCADE, verbose_name="Entidad")
#     creator = models.ForeignKey(User, on_delete=models.SET_NULL, verbose_name="Especialista", null=True)
#     title = models.TextField(max_length=1024, verbose_name="Titulo")
#     source_link = models.TextField(max_length=1024, verbose_name="Titulo")
#     description = models.TextField(
#         max_length=4096, blank=True, verbose_name="Descripción"
#     )
    

