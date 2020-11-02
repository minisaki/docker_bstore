from django.contrib import admin
from django.contrib.admin import ModelAdmin as BaseUserAdminC
from django.contrib.auth.models import User
from .models import ProfileUser
# Register your models here.


class ProfileAdmin(admin.StackedInline):
    model = ProfileUser
    can_delete = False
    verbose_name_plural = 'profile'


class UserAdmin(BaseUserAdminC):
    inlines = (ProfileAdmin,)


admin.site.unregister(User)
admin.site.register(User, UserAdmin)