from django.contrib import admin
from ui.models import User
from django.contrib.auth.models import Group

# Register your models here.


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    
    list_display = ['patient_name','patient_last_name','authorization_time','whatsapp_number', 'authorized','first_join']

    @admin.display(description='Nombre',)   
    def patient_name(self, obj):
        return obj.first_name if obj.first_name else "Sin nombre"
        
    @admin.display(description='Apellido',)   
    def patient_last_name(self, obj):
        return obj.last_name if obj.last_name else "Sin apellido"

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
             
                    self.fields = ('whatsapp_number', 'legal_id', 'first_name', 'last_name','first_join'  )
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
                
                obj.username = obj.legal_id
                obj.set_password = "password"
                obj.save()                
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
             
                    self.fields = ('whatsapp_number','legal_id','first_name', 'last_name', 'authorized','first_join' )
        else: 
            
            self.fields = ( )
                    
        return super(UserAdmin, self).change_view(request, object_id)
        