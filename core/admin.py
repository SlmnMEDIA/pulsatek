from django.contrib import admin

# Register your models here
from .models import StatusTransaction, User, Invitation

@admin.register(StatusTransaction)
class StatusAdmin(admin.ModelAdmin):
    pass


@admin.register(User)
class StatusAdmin(admin.ModelAdmin):
    pass


@admin.register(Invitation)
class InvitationAdmin(admin.ModelAdmin):
    pass