from django.core import serializers
from django.http import JsonResponse
from .models import Client


def get_clients(request):
    clients = Client.objects.filter(name__icontains=request.GET.get('q'))
    data = serializers.serialize('json', list(clients), fields=('name',))
    return JsonResponse(data, safe=False)
