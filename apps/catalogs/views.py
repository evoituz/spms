from decimal import Decimal

from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import TemplateView, DetailView

from apps.catalogs.models import *
from apps.main.models import GeneralSettings


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
        if name == 'size':
            size = profile.sizes.get(id=pk)
            size.size = value
            size.save()
        if name == 'item':
            item = ProductProfileSizeItem.objects.get(id=pk)
            if value.find(',') != -1:
                item.value = float(value.replace(',', '.'))
            else:
                item.value = float(value)
            item.save()
        if name == 'sell_price_usd':
            size = profile.sizes.get(id=pk)
            size.sell_price_usd = float(value)
            size.save()
        if name == 'sell_price_uzs':
            size = profile.sizes.get(id=pk)
            size.sell_price_uzs = float(value)
            size.save()
        if name == 'notes':
            size = profile.sizes.get(id=pk)
            size.notes = value
            size.save()

        return JsonResponse({'ok': 'success'})
        # return redirect(reverse('product-profile', None, (product_id, profile_id)))


def add_size_to_profile(request, product_id, profile_id):
    print(request)
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
                ProductProfileSizeItem.objects.create(size=size, name=k, value=v)
        return redirect(reverse('product-profile', None, (product_id, profile_id)))


class ProductProfileAdd(TemplateView):
    template_name = 'pages/products/profile_add.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        context['algorithms'] = Algorithm.objects.all()
        context['product'] = Product.objects.get(id=int(kwargs.get('product_id')))
        context['quantity_tables'] = [i for i in range(1, 51)]
        return self.render_to_response(context)

    def post(self, request, product_id):
        p = request.POST
        profile_name = p.get('profile_name')
        algorithm = p.get('algorithm')
        attr_names = p.getlist('attr_name')
        sizes = p.getlist('size')

        alg = Algorithm.objects.get(id=int(algorithm))
        product = Product.objects.get(id=product_id)
        profile = ProductProfile.objects.create(product=product, name=profile_name, algorithm=alg)
        for index, size in enumerate(sizes):
            if size:
                s = ProductProfileSize.objects.create(product_profile=profile, size=size)
                for i, attr in enumerate(attr_names):
                    if attr:
                        ProductProfileSizeItem.objects.create(
                            size=s, name=attr, value=float(p.getlist('items[{}]'.format(index + 1))[i])
                        )
        # return redirect(reverse('product-profile-add', kwargs={'product_id': product_id}))
        return redirect(reverse('products'))
