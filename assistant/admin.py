from django.contrib import admin
from django.db import models
from django import forms
from assistant.models import Video, Entity, VirtualSession, VirtualSessionVideo
from ui.models import User
from django.contrib.admin.helpers import ActionForm
from django.forms import TextInput, Textarea
from django.contrib.auth import get_permission_codename


class VirtualSessionVideoInline(admin.TabularInline):
    model = VirtualSessionVideo
    classes = ["collapse"]
    extra = 0
    formfield_overrides = {
        models.CharField: {"widget": TextInput(attrs={"size": "20"})},
        models.TextField: {"widget": Textarea(attrs={"rows": 4, "cols": 40})},
    }

class VirtualSessionForm(forms.ModelForm):
    patient = forms.ModelChoiceField(queryset=User.objects.filter(groups__name='patient'), empty_label=None)
    specialist = forms.ModelChoiceField(queryset=User.objects.filter(groups__name='specialist'), empty_label=None)
    class Meta:
        model = VirtualSession
        exclude = []

class VirtualSessionAdmin(admin.ModelAdmin):
    form = VirtualSessionForm
    inlines = [
        VirtualSessionVideoInline,
    ]
 
    list_display = ['specialist','patient', 'user_authorized','user_notified','start_time','already_started','patient_first_join','session_done','session_status_message']

    def has_change_permission(self, request, obj=None):
        codename = get_permission_codename('change', self.opts)
        has_permission = request.user.has_perm("%s.%s" % (self.opts.app_label, codename)) and  (obj.already_started == "❌" if obj else False )
        if request.user.is_superuser or has_permission:
            return True
        return False

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        groups = list(request.user.groups.all())
        group = groups[0] if len(groups)>0 else ["no group"]
        return qs.filter(specialist__groups__name = group)

    def patient_first_join(self, obj):        
        return "✅" if obj.patient.first_join  else "❌"
    patient_first_join.short_description = 'Autoización principal' 

    
    def change_view(self, request, object_id, extra_content=None):
        
        if not request.user.is_superuser:
            groups=list(request.user.groups.all())
            if len(groups)>0:
                if str(groups[0]) == "specialist":    
                    self.exclude = ('session_status_message','session_done','specialist', 'user_authorized', 'user_notified', )
            
        return super(VirtualSessionAdmin, self).change_view(request, object_id)

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
        print(request.user.groups.all())
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