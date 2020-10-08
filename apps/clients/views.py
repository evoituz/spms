import json

from django.core import serializers
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView

from .models import Client


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


@csrf_exempt
def update_client(request, id):
    name = request.POST.get('name')
    balance = request.POST.get('balance')
    client = Client.objects.get(id=id)
    client.balance = int(balance)
    client.name = name
    client.save()
    return JsonResponse({'id': client.id, 'name': client.name, 'balance': client.balance}, status=200)
