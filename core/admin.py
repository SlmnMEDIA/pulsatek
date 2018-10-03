from django.contrib import admin

# Register your models here
from .models import StatusTransaction, User

@admin.register(StatusTransaction)
class StatusAdmin(admin.ModelAdmin):
    pass


@admin.register(User)
class StatusAdmin(admin.ModelAdmin):
    pass