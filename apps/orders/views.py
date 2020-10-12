from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import ListView, TemplateView
from datetime import datetime
from apps.clients import models as clients_models
from apps.clients.models import Order, Transaction
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
        quantity_types = {'pc': 'шт', 'g': 'гр', 'm': 'м'}
        quantity_type = quantity_types[item.type_product]
        clients_models.OrderItem.objects.create(order=order, price=price, quantity=quantity + quantity_type,
                                                product_title=product_title)

    if client:
        clients_models.Transaction.objects.create(client=client, order=order, paid='payment' if paid else 'debt',
                                                  amount=order.get_total_price())
    else:
        clients_models.Transaction.objects.create(order=order, paid='payment' if paid else 'debt',
                                                  amount=order.get_total_price())

    return JsonResponse({'success': 'ok'})


class TransactionListView(ListView):
    model = Transaction
    context_object_name = 'transactions'
    template_name = 'pages/transactions/transactions_index.html'


def strint_to_datetime(string):
    return datetime.strptime(string, '%Y-%m-%d')


def transaction_list(request):
    transactions = list()

    transactions_filtered = Transaction.objects.all()
    if request.GET:
        if request.GET.get('client') != '0':
            transactions_filtered = transactions_filtered.filter(client__in=request.GET.get('client'))
        if request.GET.get('created_dt'):
            date = strint_to_datetime(request.GET.get('created_dt')[:10])
            transactions_filtered = transactions_filtered.filter(created_dt__day=date.day, created_dt__month=date.month,
                                                                 created_dt__year=date.year)
    for transaction in transactions_filtered:
        if transaction.order:
            transactions.append(
                {'id': transaction.id,
                 'created_dt': transaction.created_dt,
                 'client': {'name': transaction.client.name, 'id': transaction.client.id} if transaction.client else {},
                 'products': transaction.order.get_items_to_string(),
                 'final_sum': transaction.amount,
                 'paid': transaction.order.get_pay(),
                 'debt': transaction.order.get_debt()
                 })
        else:
            transactions.append({
                'id': transaction.id,
                'created_dt': transaction.created_dt,
                'client': {'name': transaction.client.name, 'id': transaction.client.id} if transaction.client else {},
                'products': '',
                'final_sum': transaction.amount,
                'paid': '',
                'debt': ''
            })
    return JsonResponse(transactions, safe=False)

# class OrderListView(ListView):
#     model = Order
#     context_object_name = 'orders'
#     template_name = 'pages/orders/orders_index.html'

# def get(self, request, *args, **kwargs):
#     if request.is_ajax():
#         orders = list(Order.objects.values())
#         return JsonResponse(orders, safe=False)
#     return super().get(request, *args, **kwargs)
