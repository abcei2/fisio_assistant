from django.contrib import admin
from ui.models import User

# Register your models here.


class UserAdmin(admin.ModelAdmin):
    
    list_display = ['whatsapp_number','notified', 'authorized','first_join']

admin.site.register(User, UserAdmin)