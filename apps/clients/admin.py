from django.contrib import admin
from .models import Client, Transaction, OrderItem, Order

admin.site.register(Client)
admin.site.register(Transaction)
admin.site.register(OrderItem)
admin.site.register(Order)
