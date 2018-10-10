from import_export import resources


from .models import User


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