from django.contrib import admin
from django.db import models
from django import forms
from assistant.models import Video, Entity, VirtualSession, VirtualSessionVideo, VirtualSessionMessages
from ui.models import User
from django.contrib.admin.helpers import ActionForm
from django.forms import TextInput, Textarea
from django.contrib.auth import get_permission_codename
from django.utils.safestring import mark_safe


EXCLUDE_FIELDS=('user_presession_notified','session_status_message','session_done','specialist', 'user_authorized', 'user_notified','last_commentary_message_section','user_presession_last_answer','is_session_expired' )
class VirtualSessionMessagesInline(admin.TabularInline):
    model = VirtualSessionMessages
    classes = ["collapse"]
    extra = 0
    formfield_overrides = {
        models.CharField: {"widget": TextInput(attrs={"size": "20"})},
        models.TextField: {"widget": Textarea(attrs={"rows": 4, "cols": 40})},
    }


class VirtualSessionVideoInline(admin.TabularInline):
    model = VirtualSessionVideo
    classes = ["collapse"]
    extra = 0
    formfield_overrides = {
        models.CharField: {"widget": TextInput(attrs={"size": "20"})},
        models.TextField: {"widget": Textarea(attrs={"rows": 4, "cols": 40})},
    }
    
      
    readonly_fields = ['video_title']

    @admin.display(description='Link del video')
    def video_title(self, obj):
        return mark_safe('<a href="%s">%s</a>' % (obj.video.source_link,obj.video.source_link))

class VirtualSessionForm(forms.ModelForm):
    patient = forms.ModelChoiceField(queryset=User.objects.filter(groups__name='patient'), empty_label=None)
    # specialist = forms.ModelChoiceField(queryset=User.objects.filter(groups__name='specialist'), empty_label=None)
    class Meta:
        model = VirtualSession
        exclude = []

@admin.register(VirtualSession)
class VirtualSessionAdmin(admin.ModelAdmin):
    ordering = ['-start_time']
    form = VirtualSessionForm
    inlines = [
        VirtualSessionVideoInline, 
        VirtualSessionMessagesInline
    ]
 
    list_display = ['specialist','patient', 'user_authorized','user_notified','start_time','already_started_icon','patient_first_join','session_done','session_expired_icon','session_status_message']

    def has_change_permission(self, request, obj=None):
        '''
            specialist can change session only if haven't started
        '''
        codename = get_permission_codename('change', self.opts)
        has_permission = request.user.has_perm("%s.%s" % (self.opts.app_label, codename)) and  (not obj.already_started  if obj else False )
        if request.user.is_superuser or has_permission:
            return True
        return False

    def get_queryset(self, request):
        '''
            showing up just specialist created sessions
        '''
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(specialist=request.user)

    @admin.display(description='Autoizaci??n principal',)   
    def patient_first_join(self, obj):       
        '''
            when a patient have joined on sand box of filling some concent 
            to recieve notifications and messages.
        ''' 
        return "???" if obj.patient.first_join  else "???"

    @admin.display(description='Sesi??n iniciada',)   
    def already_started_icon(self, obj):       
        '''
            when a patient have joined on sand box of filling some concent 
            to recieve notifications and messages.
        ''' 
        return "???" if obj.already_started  else "???"
        
    @admin.display(description='Sesi??n caducada',)   
    def session_expired_icon(self, obj):       
        '''
            when a session expires
        ''' 
        return "???" if obj.session_expired  else "???"

    
    def change_view(self, request, object_id, extra_content=None):
        
        if not request.user.is_superuser:
            groups=list(request.user.groups.all())
            if len(groups)>0:
                if str(groups[0]) == "specialist":    
                    self.exclude = EXCLUDE_FIELDS
            
        return super(VirtualSessionAdmin, self).change_view(request, object_id)

    def add_view(self, request, extra_content=None):
        
        if not request.user.is_superuser:
            groups=list(request.user.groups.all())
            if len(groups)>0:
                if str(groups[0]) == "specialist":    
                    self.exclude = EXCLUDE_FIELDS
        return super(VirtualSessionAdmin, self).add_view(request)

    def save_model(self, request, obj, form, change):
        """
            when user are specialist save himself
        """
        if len(list(request.user.groups.all()))>0:
            if str(list(request.user.groups.all())[0]) == "specialist":
                obj.specialist = request.user      
        obj.save()

@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ['title', 'video_source_link']
    
    def video_source_link(self, obj):
        return mark_safe('<a href="%s">%s</a>' % (obj.source_link,obj.source_link))
    video_source_link.short_description = 'Icon'
    video_source_link.allow_tags = True
 
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
        groups=list(request.user.groups.all())
        if len(groups)>0:
            if str(groups[0]) == "specialist":
                obj.entity = Entity.objects.all()[0]
                obj.creator = request.user      
        obj.save()

    
@admin.register(Entity)
class EntityAdmin(admin.ModelAdmin):
    
    def add_view(self, request, extra_content=None):
        
        return super(EntityAdmin, self).add_view(request)

