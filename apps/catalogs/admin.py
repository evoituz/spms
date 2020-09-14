from django.contrib import admin

from apps.catalogs.models import *

admin.site.register(Product)
admin.site.register(ProductProfile)
admin.site.register(ProductProfileSize)
admin.site.register(ProductProfileSizeItem)
