from django.contrib import admin
from ui.models import User

# Register your models here.


class UserAdmin(admin.ModelAdmin):
    pass
admin.site.register(User, UserAdmin)