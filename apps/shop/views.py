from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic import ListView

from apps.stock.models import Stock, StockCategory


class ShopProductListView(ListView):
    model = Stock
    template_name = 'pages/shop/shop_index.html'

    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            queryset = list(Stock.objects.values('id', 'category_id', 'profile_name', 'size', 'quantity', 'type_product', 'price_sell'))
            return JsonResponse(queryset, safe=False)
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = StockCategory.objects.all()
        return context
