from django.db import models
from ui.models import Entity, User
from core.model_utils import BaseModel  
from django.utils.functional import cached_property
from django.utils import timezone
 

class Video(BaseModel):    
    entity = models.ForeignKey(Entity, on_delete=models.CASCADE, verbose_name="Entidad")
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, verbose_name="Especialista", null=True)
    title = models.CharField(max_length=256, verbose_name="Titulo del video")
    source_link = models.URLField(max_length=1024, verbose_name="Link del recurso")
    description = models.TextField(
        max_length=4096, blank=True, verbose_name="Descripción"
    )
    
class VirtualSession(BaseModel):    
    patient = models.ForeignKey(User, on_delete=models.SET_NULL, verbose_name="Paciente", related_name='patient', null=True)
    specialist = models.ForeignKey(User, on_delete=models.SET_NULL, verbose_name="Especialista",related_name='specialist', null=True)
    description_message = models.TextField(max_length=1024, verbose_name="Mensaje de asistencia", blank = True, default="")
    start_time = models.DateTimeField(auto_now_add=False, verbose_name="Tiempo de Inicio" )    
    session_status_message = models.CharField(max_length=256, verbose_name="Stado de la sesión", default="La sesión ha sido programada.")
    session_done = models.BooleanField(default=False, verbose_name="La sesión ha finalizado")
    user_notified = models.BooleanField(default=False, verbose_name="Notificación al usuario")
    user_authorized = models.BooleanField(default=False, verbose_name="Confirmación del usuario")

    
    @cached_property
    def already_started(self):
        return "✅" if self.start_time < timezone.now()  else "❌"
       
class VirtualSessionVideo(BaseModel):
    session = models.ForeignKey(VirtualSession, on_delete=models.SET_NULL, verbose_name="Id mensaje asignado", null=True)
    video = models.ForeignKey(Video, on_delete=models.SET_NULL, verbose_name="Video de ejercicios asignado", null=True)


    

