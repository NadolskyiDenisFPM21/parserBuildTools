from django.contrib import admin

from sites.models import Site, SiteGoods, Direction

from import_export.admin import ImportExportActionModelAdmin
from import_export import resources


class SiteResource(resources.ModelResource):
    class Meta:
        model = Site


class SiteGoodsResource(resources.ModelResource):
    class Meta:
        model = SiteGoods


@admin.register(SiteGoods)
class SiteGoodsAdmin(ImportExportActionModelAdmin):
    resource_class = SiteGoodsResource
    list_display = ('goods', 'site', 'price_on_site')


class SiteGoodsInline(admin.TabularInline):
    model = SiteGoods
    extra = 1  # Количество пустых форм для добавления новых объектов


# Register your models here.
@admin.register(Site)
class SiteAdmin(ImportExportActionModelAdmin):
    resource_class = SiteResource
    list_display = ('name', 'link')
    inlines = [SiteGoodsInline, ]


@admin.register(Direction)
class DirectionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
