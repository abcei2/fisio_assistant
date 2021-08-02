from django.contrib import admin
from ui.models import User

# Register your models here.


class UserAdmin(admin.ModelAdmin):
    
    list_display = ['whatsapp_number','notified', 'authorized','first_join']
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return query_session_timer
        return qs.filter(groups__name = "patient")

admin.site.register(User, UserAdmin)