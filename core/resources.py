from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget

from .models import User, Telegram


class UserResource(resources.ModelResource):
    class Meta:
        model = User
        fields = [
            'email', 'first_name', 'last_name', 'saldo', 'limit',
        ]
        import_id_fields = ['email']
        skip_unchanged = True
        report_skipped = False
        export_order = ('email', 'first_name', 'last_name', 'saldo')


class TelegramResource(resources.ModelResource):
    email = fields.Field(column_name='user', attribute='user', widget=ForeignKeyWidget(User, 'email'))
    class Meta:
        model = Telegram
        fields = [
            'telegram', 'email'
        ]
        import_id_fields = ['telegram']
        skip_unchanged = True
        report_skipped = False
        export_order = ('telegram',)