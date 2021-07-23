from django.db import models
from ui.models import Entity, Specialist
# Create your models here.


class Videos(BaseModel):
    
    entity = models.ForeignKey(Entity, on_delete=models.CASCADE, verbose_name="Entidad")
    creator = models.ForeignKey(Specialist, on_delete=models.SET_NULL, verbose_name="Especialista")
    title = models.TextField(max_length=1024, verbose_name="Titulo")
    source_link = models.TextField(max_length=1024, verbose_name="Titulo")
    description = models.TextField(
        max_length=4096, blank=True, verbose_name="Descripción"
    )
    

