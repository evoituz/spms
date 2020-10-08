from django.contrib import admin
from .models import Client, Transaction

admin.site.register(Client)
admin.site.register(Transaction)
