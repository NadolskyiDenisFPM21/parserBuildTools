from admin_numeric_filter.admin import RangeNumericFilter
from django.contrib import admin

from import_export.admin import ImportExportActionModelAdmin
from import_export.widgets import DecimalWidget
from import_export import resources, fields

from goods.models import Goods


class CustomDecimalWidget(DecimalWidget):
    def clean(self, value, row=None, **kwargs):
        # Замена запятой на точку в значениях чисел
        if value and isinstance(value, str):
            value = value.replace(',', '.')
        return super().clean(value, row, **kwargs)


class GoodsResource(resources.ModelResource):
    price = fields.Field(
        column_name='price',
        attribute='price',
        widget=CustomDecimalWidget()
    )

    class Meta:
        model = Goods


@admin.register(Goods)
class GoodsAdmin(ImportExportActionModelAdmin):
    resource_class = GoodsResource
    fields = ('sku', 'name', 'price', 'directions')
    list_display = ('id', 'sku', 'name', 'price')
    search_fields = ('id', 'sku', 'name', 'price')
    list_filter = (
        'sku',
        ('price', RangeNumericFilter),
    )
