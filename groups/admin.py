from django.contrib import admin
from . import models
# Register your models here.
from django.contrib.auth import get_user_model
User = get_user_model()


class GroupMemberInline(admin.TabularInline):
    model = models.GroupMember

class GroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'description','created_at')
    inlines = (GroupMemberInline,)



admin.site.register(models.Group, GroupAdmin)
