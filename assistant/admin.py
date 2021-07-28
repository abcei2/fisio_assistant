from django.contrib import admin
from assistant.models import Videos, Entity
from django.contrib.admin.helpers import ActionForm
from django import forms


class VideosAdmin(admin.ModelAdmin):
    list_display = ['title', 'source_link']
    def add_view(self, request, extra_context=None):
        
        extra_context = extra_context or {}
        groups=list(request.user.groups.all())
        if len(groups)>0:
            if str(groups[0]) == "specialist":
                
                self.exclude = ('entity','creator', )
            
            
        return super(VideosAdmin, self).add_view(request)
    
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
admin.site.register(Videos, VideosAdmin)