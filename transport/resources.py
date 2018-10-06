from import_export import resources, fields
from import_export.widgets import ForeignKeyWidget


from .models import Product, Operator, Server

class ProductResource(resources.ModelResource):
    operator = fields.Field(column_name='operator', attribute='operator', widget=ForeignKeyWidget(Operator, 'operator'))
    server = fields.Field(column_name='server', attribute='server', widget=ForeignKeyWidget(Server, 'code'))
    class Meta:
        model = Product
        import_id_fields = ['product_code']
        fields = [
            'product_code', 'product_name', 'operator',
            'product_type', 'server', 'title', 'nominal', 
            'price', 'description', 'additional_info'
        ]
        skip_unchanged = True
        report_skipped = False
        export_order = ('product_code', 'product_name', 'operator')


class OperatorResource(resources.ModelResource):
    class Meta:
        model = Operator
        fields = [
            'operator', 'parse'
        ]
        skip_unchanged = True
        report_skipped = False
        export_order = ['operator']


class ServerResource(resources.ModelResource):
    class Meta:
        model = Server
        fields = [
            'code', 'product_name', 'price'
        ]
        export_order = ['code', 'product_name', 'price']
        skip_unchanged = True
        report_skipped = False
