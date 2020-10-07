from urllib.parse import unquote

from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import ListView, DetailView, DeleteView

from apps.stock.models import Stock, StockCategory


class StockListView(ListView):
    model = Stock
    template_name = 'pages/stock/stock_index.html'

    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            queryset = list(self.model.objects.values())
            return JsonResponse(queryset, safe=False)
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = StockCategory.objects.all()
        return context


def fetch_data_from_request(request):
    data = request.body.decode('utf-8').split('&')
    data_dict = {d.split('=')[0]: unquote(d.split('=')[-1]).replace('+', ' ') for d in data}
    return data_dict


def stock_control(request):
    if request.method == 'DELETE':
        print('DELETE')
        data = fetch_data_from_request(request)
        Stock.objects.get(pk=data['id']).delete()
        return JsonResponse(data)

    if request.method == 'PUT':
        print('PUT')
        data = fetch_data_from_request(request)
        stock = Stock.objects.get(pk=data.get('id'))
        stock.__dict__.update(data)
        stock.save()
        return JsonResponse(data)

    if request.method == 'POST':
        print('POST')
        data = request.POST
        stock_category = StockCategory.objects.get(pk=data.get('category_id'))
        stock = Stock.objects.create(
            category=stock_category,
            profile_name=data.get('profile_name', ''),
            size=data.get('size'),
            quantity=data.get('quantity', 0),
            type_product=data.get('type_product', 'pc'),
            price_purchase=data.get('price_purchase', 0),
            price_arrival=data.get('price_arrival', 0),
            price_sell=data.get('price_sell'),
        )
        result = {k: v for k, v in stock.__dict__.items() if k != '_state'}
        return JsonResponse(result)


def get_stock_categories(request):
    if request.is_ajax():
        if request.method == 'GET':
            stock_category_list = list(StockCategory.objects.values())
            return JsonResponse(stock_category_list, safe=False)

        if request.method == 'POST':
            stock_category, _ = StockCategory.objects.get_or_create(name=request.POST.get('name'))
            result = {k: v for k, v in stock_category.__dict__.items() if k != '_state'}
            return JsonResponse(result)

        if request.method == 'DELETE':
            print('DELETE')
            data = fetch_data_from_request(request)
            StockCategory.objects.get(pk=data['id']).delete()
            return JsonResponse(data)

        if request.method == 'PUT':
            print('PUT')
            data = fetch_data_from_request(request)
            stock = StockCategory.objects.get(pk=data.get('id'))
            stock.__dict__.update(data)
            stock.save()
            return JsonResponse(data)

    return redirect(reverse('stock'))
