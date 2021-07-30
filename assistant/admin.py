from django.contrib import admin
from django.db import models
from assistant.models import Video, Entity, VirtualSession, VirtualSessionVideo
from django.contrib.admin.helpers import ActionForm
from django.forms import TextInput, Textarea


class VirtualSessionVideoInline(admin.TabularInline):
    model = VirtualSessionVideo
    classes = ["collapse"]
    extra = 0
    formfield_overrides = {
        models.CharField: {"widget": TextInput(attrs={"size": "20"})},
        models.TextField: {"widget": Textarea(attrs={"rows": 4, "cols": 40})},
    }
    
class VirtualSessionAdmin(admin.ModelAdmin):
    inlines = [
        VirtualSessionVideoInline,
    ]
    
    list_display = ['specialist','patient', 'user_authorized','user_notified','start_time','already_started','patient_first_join','session_done','session_status_message']

    def patient_first_join(self, obj):        
        return "✅" if obj.patient.first_join  else "❌"
    patient_first_join.short_description = 'Autoización principal' 

    def add_view(self, request, extra_content=None):
        groups=list(request.user.groups.all())
        if len(groups)>0:
            if str(groups[0]) == "specialist":    
                self.exclude = ('session_status_message','session_done','specialist', 'user_authorized', 'user_notified', )
            else:                            
                self.exclude = ('session_status_message','session_done','user_authorized', 'user_notified', )
        return super(VirtualSessionAdmin, self).add_view(request)
    def save_model(self, request, obj, form, change):
        """
        Given a model instance save it to the database.
        """
        if str(list(request.user.groups.all())[0]) == "specialist":
            obj.specialist = request.user      
        obj.save()

class VideoAdmin(admin.ModelAdmin):
    list_display = ['title', 'source_link']
    def add_view(self, request, extra_context=None):
        
        extra_context = extra_context or {}
        groups=list(request.user.groups.all())
        if len(groups)>0:
            if str(groups[0]) == "specialist":
                
                self.exclude = ('entity','creator', )
            
            
        return super(VideoAdmin, self).add_view(request)
    
    def save_model(self, request, obj, form, change):
        """
        Given a model instance save it to the database.
        """
        if str(list(request.user.groups.all())[0]) == "specialist":
            obj.entity = Entity.objects.all()[0]
            obj.creator = request.user      
        obj.save()

    
class EntityAdmin(admin.ModelAdmin):
    
    def add_view(self, request, extra_content=None):
        
        return super(EntityAdmin, self).add_view(request)


admin.site.register(Entity, EntityAdmin)
admin.site.register(Video, VideoAdmin)
admin.site.register(VirtualSession, VirtualSessionAdmin)