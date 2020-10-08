import json
from datetime import datetime

from django.core import serializers
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, TemplateView, DetailView

from .models import Client, OrderItem, Transaction


def get_clients(request):
    clients = Client.objects.filter(name__icontains=request.GET.get('q'))
    data = serializers.serialize('json', list(clients), fields=('name',))
    return JsonResponse(data, safe=False)


class ClientsListView(ListView):
    model = Client
    template_name = 'pages/clients/clients_index.html'

    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            queryset = list(self.model.objects.values('id', 'name', 'balance'))
            return JsonResponse(queryset, safe=False)
        return super().get(request, *args, **kwargs)


class ClientView(DetailView):
    model = Client
    template_name = 'pages/clients/client_page.html'

    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            queryset = list(
                self.model.objects.get(id=self.kwargs['pk']).order_set.all().values('items__product_title',
                                                                                    'items__price',
                                                                                    'created_dt',
                                                                                    'transaction__paid'))
            for q in queryset:
                q['paid_price'] = 1
                if q['transaction__paid'] == 'payment':
                    q['paid_price'] = q['items__price']
                    q['debt_price'] = 0
                else:
                    q['paid_price'] = 0
                    q['debt_price'] = q['items__price']
            return JsonResponse(queryset, safe=False)
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ClientView, self).get_context_data(**kwargs)
        context['user'] = Client.objects.get(id=self.kwargs['pk'])
        return context


class TransactionView(TemplateView):
    model = Transaction

    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            queryset = list(
                self.model.objects.filter(client_id=self.request.GET.get('url_id'), order__isnull=True).values(
                    'created_dt',
                    'amount',
                ))
            return JsonResponse(queryset, safe=False)

    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            print(request.POST)
            client = Client.objects.get(id=kwargs['pk'])
            client.balance += int(request.POST.get('amount'))
            client.save()
            transaction = self.model.objects.create(amount=request.POST.get('amount'), client=client)

            return JsonResponse(
                {'amount': transaction.amount, 'created_dt': transaction.created_dt.strftime("%d.%m.%Y %H:%M")},
                status=200)


@csrf_exempt
def update_client(request, id):
    name = request.POST.get('name')
    balance = request.POST.get('balance')
    client = Client.objects.get(id=id)
    client.balance = int(balance)
    client.name = name
    client.save()
    return JsonResponse({'id': client.id, 'name': client.name, 'balance': client.balance}, status=200)
