from django.db import models
from ui.models import Entity, User
from core.model_utils import BaseModel  
from django.utils.functional import cached_property
from django.utils import timezone
 
MINUTES_BETWEEN_BOT_ANSWER = 5

class Video(BaseModel):    
    entity = models.ForeignKey(Entity, on_delete=models.CASCADE, verbose_name="Entidad")
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, verbose_name="Especialista", null=True)
    title = models.CharField(max_length=256, verbose_name="Titulo del video")
    source_link = models.URLField(max_length=1024, verbose_name="Link del recurso")
    description = models.TextField(
        max_length=4096, blank=True, verbose_name="Descripción"
    )
    def __str__(self):
        return f"{self.title}"
    
class VirtualSession(BaseModel):    
    patient = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Paciente", related_name='patient', null=True)
    specialist = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Especialista",related_name='specialist', null=True)
    description_message = models.TextField(max_length=1024, verbose_name="Mensaje de asistencia", blank = True, default="")
    session_items = models.TextField(max_length=1024, verbose_name="Elementos necesarios para le sesión", blank = True, default="")
    start_time = models.DateTimeField(auto_now_add=False, verbose_name="Tiempo de Inicio" )    
    session_duration = models.IntegerField(verbose_name="Duración de la sesión en minutos", default=60 )    


    session_status_message = models.CharField(max_length=256, verbose_name="Stado de la sesión", default="La sesión ha sido programada.")
    session_done = models.BooleanField(default=False, verbose_name="La sesión ha finalizado")
    is_session_expired = models.BooleanField(default=False, verbose_name="Bandera para indicar si una sesión expiró o no")
    
    user_presession_notified = models.BooleanField(default=False, verbose_name="Notificación al usuario 12 horas antes de la sesión")
    user_presession_last_answer = models.DateTimeField( verbose_name="Fecha en la que se le responde al usuario despues de un comentario entre sesión",
                                                             null=True)

    user_notified = models.BooleanField(default=False, verbose_name="Notificación al usuario")
    user_authorized = models.BooleanField(default=False, verbose_name="El usuario confirma la sesión")

    last_commentary_message_section = models.BooleanField(default=False, verbose_name="Indica cuando un usuario puede ingresar comentario final")
    
    @cached_property
    def bot_answer(self):
        if  self.user_presession_last_answer:
            return True if self.user_presession_last_answer + timezone.timedelta(minutes=MINUTES_BETWEEN_BOT_ANSWER)  < timezone.now()    else False
        else:
            return True

    @cached_property
    def already_started(self):
        return True if timezone.now() > self.start_time  else False
        
    @cached_property
    def session_expired(self):
        if  timezone.now() > self.start_time + timezone.timedelta(minutes=self.session_duration) and not self.session_done:
            self.session_done = True
            self.is_session_expired=True
            self.save()
            self.session_status_message += "\nLa sesión ha expirado."
   
        return  self.is_session_expired
       
    @cached_property
    def time_to_notify(self):
        if (timezone.now() > self.start_time-timezone.timedelta(hours=12) 
            and timezone.now() < self.start_time) and not self.user_presession_notified:
            return True
        else:
            return False
            
    @cached_property
    def time_before_start(self):
        if self.start_time>timezone.now():
            time_to_start = str(self.start_time-timezone.now())  
            time_to_start = time_to_start.split(".")
            time_to_start = time_to_start[0].split(":") # Dropping seconds, splitting Hours and minutes
            hours = time_to_start[0]
            minutes = time_to_start[1]
            hours_plural=""
            minutes_plural=""
            
            if minutes[0]=="0":
                minutes = minutes[1]
            if minutes=="1":
                minutes_plural=""
            else:
                minutes_plural="s"
            if hours=="1":
                hours_plural=""
            else:
                hours_plural="s"
                  
            if hours == "0":
                if minutes == "0":
                    return f"en menos de un minuto"
                else:
                    return f"{minutes} minuto{minutes_plural}"
            elif hours != "0" :
                if minutes == "0":
                    return f"{hours} hora{hours_plural}"
                else:
                    return f"{hours} hora{hours_plural} y {minutes} minuto{minutes_plural}"
        else:
            return "unos momentos"
     
      

class VirtualSessionVideo(BaseModel):
    session = models.ForeignKey(VirtualSession, on_delete=models.SET_NULL, verbose_name="Id mensaje asignado", null=True)
    video = models.ForeignKey(Video, on_delete=models.SET_NULL, verbose_name="Video de ejercicios asignado", null=True)
    
    def __str__(self):
        return f"{self.video.title}"
            


class VirtualSessionMessages(BaseModel):
    session = models.ForeignKey(VirtualSession, on_delete=models.CASCADE, verbose_name="Id de la sesión", null=True)
    message = models.CharField(max_length=256, verbose_name="Respuesta del paciente.")


    

