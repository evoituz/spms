from django.http import JsonResponse
from django.shortcuts import render
from apps.clients import models as clients_models
from apps.stock import models as stock_models
import json


def create_order(request):
    data = request.POST

    paid = True if data.get('paid') == 'true' else False

    if data.get('customer') != '0':  # check if user is even inputted
        if data.get('customer').isdigit():  # check if user already exists
            client, _ = clients_models.Client.objects.get_or_create(id=data.get('customer'))
        else:
            client = clients_models.Client.objects.create(name=data.get('customer'), balance=0)
        if not paid:
            client.balance -= int(data.get('total_price'))
            client.save(update_fields=['balance', ])
    else:
        client = None
    if client:
        order = clients_models.Order.objects.create(client=client)
    else:
        order = clients_models.Order.objects.create()

    for item in data.getlist('items[]'):
        item = json.loads(item)
        price = item['price_sell']
        quantity = item['quantity']
        item = stock_models.Stock.objects.get(id=item['id'])
        item.quantity -= int(quantity)
        item.save(update_fields=['quantity', ])
        product_title = item.category.name + ' ' + item.profile_name + ' ' + item.size
        clients_models.OrderItem.objects.create(order=order, price=price, quantity=quantity,
                                                product_title=product_title)

    if client:
        clients_models.Transaction.objects.create(client=client, order=order, paid='payment' if paid else 'debt',
                                                  amount=order.get_total_price())
    else:
        clients_models.Transaction.objects.create(order=order, paid=paid,
                                                  amount=order.get_total_price())

    return JsonResponse({'success': 'ok'})
