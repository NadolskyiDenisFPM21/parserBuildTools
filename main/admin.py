from django.contrib import admin
from .models import ParseReport


@admin.register(ParseReport)
class ParseReportAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'created_at')
