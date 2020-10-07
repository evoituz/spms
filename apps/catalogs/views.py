from decimal import Decimal

from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import TemplateView, DetailView

from apps.catalogs.models import *
from apps.stock.models import Stock, StockCategory


def checking_value(val):
    result = val
    if val.find(',') != -1:
        result = val.replace(',', '.')
    return float(result)


def create_stock_meter(size_obj):
    """Добавляет в склад товар - только если заполнены поля tone и sell_price_uzs"""
    if size_obj.get_meter() != 0 and size_obj.sell_price_uzs:  # Не заполнено поле "tone" в объекте моделя ProductProfileSize
        product_category = size_obj.product_profile.product
        profile = size_obj.product_profile

        category, _ = StockCategory.objects.get_or_create(name=product_category.name)

        values_for_update = {
            'category': category,
            'profile_name': profile.name,
            'size': size_obj.size,
            'quantity': size_obj.get_meter(),
            'type_product': 'm',
            'price_sell': size_obj.sell_price_uzs,
        }
        stock, _ = Stock.objects.update_or_create(
            category=category, profile_name=profile.name, size=size_obj.size,
            defaults=values_for_update
        )


class PriceListViews(TemplateView):
    template_name = 'pages/products/price_list.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        context['products'] = Product.objects.all()
        return self.render_to_response(context)

    def post(self, request):
        data = request.POST.get('product_name')
        if data:
            Product.objects.create(name=data)
        return redirect(reverse('products'))


class ProductProfileViews(DetailView):
    object = ProductProfile
    pk_url_kwarg = 'profile_id'
    template_name = 'pages/products/profile_page.html'
    product_id = None
    profile_id = None

    def get(self, request, *args, **kwargs):
        self.product_id = kwargs.get('product_id')
        self.profile_id = kwargs.get('profile_id')
        context = self.get_context_data(**kwargs)
        product = Product.objects.get(id=int(self.product_id))
        context['profile'] = ProductProfile.objects.get(product=product, id=int(self.profile_id))
        sizes = []
        for size in context['profile'].sizes.all():
            data = {
                'size': size.size,
                'size_id': size.id,
                'size_tone': size.tone,
                'algorithm': size.get_algorithm(),
                'uzs': size.get_uzs(),
                'sell_price_usd': size.sell_price_usd,
                'sell_price_uzs': size.sell_price_uzs,
                'notes': size.notes,
                'items': size.items.values(),
            }
            sizes.append(data)
        context['sizes'] = sizes
        context['product'] = product
        return self.render_to_response(context)

    def get_queryset(self):
        product = Product.objects.get(id=self.profile_id)
        profile = ProductProfile.objects.get(product=product, id=self.profile_id)
        return profile

    def post(self, request, *args, **kwargs):
        print(request.POST)
        product_id = kwargs.get('product_id')
        profile_id = kwargs.get('profile_id')
        name = request.POST.get('name')
        value = request.POST.get('value')
        pk = int(request.POST.get('pk'))

        profile = ProductProfile.objects.get(product__id=int(product_id), id=int(profile_id))
        size = profile.sizes.get(id=pk)
        if name == 'size':
            size.size = value
        if name == 'item':
            item = ProductProfileSizeItem.objects.get(id=pk)
            if value.find(',') != -1:
                item.value = float(value.replace(',', '.'))
            else:
                item.value = float(value)
            item.save()
        if name == 'sell_price_usd':
            size.sell_price_usd = float(value)
        if name == 'sell_price_uzs':
            size.sell_price_uzs = float(value)
        if name == 'notes':
            size.notes = value
        if name == 'tone':
            size.tone = int(value)
        size.save()

        list_names = ['sell_price_uzs', 'tone']
        if name in list_names:
            create_stock_meter(size)

        return JsonResponse({'ok': 'success'})
        # return redirect(reverse('product-profile', None, (product_id, profile_id)))


def add_size_to_profile(request, product_id, profile_id):
    if request.POST:
        p = request.POST
        profile = ProductProfile.objects.get(product_id=product_id, id=profile_id)
        size = None
        for k, v in p.items():
            if k == 'csrfmiddlewaretoken':
                continue
            elif k == 'size':
                size = ProductProfileSize.objects.create(product_profile=profile, size=v)
            else:
                ProductProfileSizeItem.objects.create(size=size, name=k, value=checking_value(v))
        return redirect(reverse('product-profile', None, (product_id, profile_id)))


class ProductProfileAdd(TemplateView):
    template_name = 'pages/products/profile_add.html'

    def get(self, request, *args, **kwargs):
        print('auth', request.user.is_authenticated)
        print('super', request.user.is_superuser)
        if request.user.is_authenticated and request.user.is_superuser:
            context = self.get_context_data(**kwargs)
            context['algorithms'] = Algorithm.objects.all()
            context['product'] = Product.objects.get(id=int(kwargs.get('product_id')))
            context['quantity_tables'] = [i for i in range(1, 51)]
            return self.render_to_response(context)
        return redirect(reverse('products'))

    def post(self, request, product_id):
        p = request.POST
        profile_name = p.get('profile_name')
        algorithm = p.get('algorithm')
        attr_names = p.getlist('attr_name')
        sizes = p.getlist('size')

        alg = Algorithm.objects.get(id=int(algorithm))
        product = Product.objects.get(id=product_id)
        profile = ProductProfile.objects.create(product=product, name=profile_name, algorithm=alg)
        try:
            for index, size in enumerate(sizes):
                if size:
                    s = ProductProfileSize.objects.create(product_profile=profile, size=size)
                    for i, attr in enumerate(attr_names):
                        if attr:
                            ProductProfileSizeItem.objects.create(
                                size=s, name=attr, value=checking_value(p.getlist('items[{}]'.format(index + 1))[i])
                            )
        except Exception as e:
            print(e)
            profile.delete()
        # return redirect(reverse('product-profile-add', kwargs={'product_id': product_id}))
        return redirect(reverse('products'))
