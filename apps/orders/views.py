from django.http import JsonResponse
from django.shortcuts import render
from apps.clients import models as clients_models


def create_order(request):
    print('asd')
    print(request.POST)
    data = request.POST
    print(data.getlist('items[]'))
    # client = clients_models.Client.objects.get_or_create(
    #     name=data.get('customer') if data.get['customer'] else 'Anonymous')
    # order = clients_models.Order.objects.create(client=client)
    for v in data.items():
        print(v)

    return JsonResponse({'success': 'ok'})
