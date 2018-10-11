from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

# Register your models here
from .models import StatusTransaction, User, Invitation, SiteMaster, MessagePost, Telegram
from .resources import UserResource, TelegramResource

@admin.register(StatusTransaction)
class StatusAdmin(admin.ModelAdmin):
    pass


@admin.register(Telegram)
class TelegramAdmin(ImportExportModelAdmin):
    resource_class = TelegramResource
    list_display = ['user', 'telegram']


@admin.register(User)
class StatusAdmin(ImportExportModelAdmin):
    list_display = [
        'email', 'full_name', 'is_active', 'is_superuser', 'is_staff', 'is_agen',
        'saldo', 'limit', 'pin', 'get_telegram', 'last_login'
    ]
    resource_class = UserResource


@admin.register(Invitation)
class InvitationAdmin(admin.ModelAdmin):
    pass


@admin.register(SiteMaster)
class SiteMasterAdmin(admin.ModelAdmin):
    list_display = [
        'code', 'status', 'keterangan'
    ]

    
@admin.register(MessagePost)
class MessagePostAdmin(admin.ModelAdmin):
    list_display = [
        'subject', 'created_by', 'schedule', 'closed', 'timestamp', 'update'
    ]