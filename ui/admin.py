from django.contrib import admin
from ui.models import User
from django.contrib.auth.models import Group

# Register your models here.


class UserAdmin(admin.ModelAdmin):
    
    list_display = ['authorization_time','whatsapp_number','notified', 'authorized','first_join']
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(groups__name = "patient")

    def add_view(self, request, extra_content=None):      
        print(request.user.is_superuser, request.user)  
        if not request.user.is_superuser:
            groups=list(request.user.groups.all())
            if len(groups)>0:
                if str(groups[0]) == "specialist":    
             
                    self.fields = ('whatsapp_number','legal_id', 'password','username','first_join'  )
        else: 
            
            self.fields = ( )
                    
        return super(UserAdmin, self).add_view(request)

    def save_model(self, request, obj, form, change):
        """
            when user are specialist save himself
        """
        
        groups=list(request.user.groups.all())
        obj.save()    
        if len(groups)>0:
            if str(groups[0]) == "specialist":                
                my_group = Group.objects.get(name='patient')  
                my_group.user_set.add(obj)
        else:              
            my_group = Group.objects.get(name='specialist')  
            my_group.user_set.add(obj)
        
    def change_view(self, request, object_id, extra_content=None):
        if not request.user.is_superuser:
            groups=list(request.user.groups.all())
            if len(groups)>0:
                if str(groups[0]) == "specialist":    
             
                    self.fields = ('whatsapp_number','legal_id', 'password','notified', 'authorized','first_join' )
        else: 
            
            self.fields = ( )
                    
        return super(UserAdmin, self).change_view(request, object_id)
admin.site.register(User, UserAdmin)