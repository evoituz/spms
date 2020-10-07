from django.contrib import admin

from apps.stock.models import StockCategory, Stock

admin.site.register(StockCategory)
admin.site.register(Stock)
