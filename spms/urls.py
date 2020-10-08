from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from apps.catalogs import views as catalog_views
from apps.main import views as main_views
from apps.stock import views as stock_views
from apps.shop import views as shop_views
from apps.orders import views as order_views
from apps.clients import views as clients_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('settings/', main_views.SettingsViews.as_view(), name='settings'),

    path('product/<int:product_id>/profile/<int:profile_id>/', catalog_views.ProductProfileViews.as_view(),
         name='product-profile'),
    path('product/<int:product_id>/profile/add/', catalog_views.ProductProfileAdd.as_view(),
         name='product-profile-add'),
    path('product/<int:product_id>/profile/<int:profile_id>/size/add/', catalog_views.add_size_to_profile,
         name='add-size-to-profile'),
    path('products/', catalog_views.PriceListViews.as_view(), name='products'),

    path('stock/control/', stock_views.stock_control, name='stock-control'),
    path('stock/categories/control/', stock_views.get_stock_categories, name='stock-categories-control'),
    path('stock/', stock_views.StockListView.as_view(), name='stock'),

    path('shop/', shop_views.ShopProductListView.as_view(), name='shop'),

    path('', main_views.HomePageViews.as_view(), name='home-page'),

    path('order/', order_views.create_order, name='create-order'),

    path('clients/get-clients/', clients_views.get_clients, name='get-clients'),
    path('clients/update-client/<int:id>/', clients_views.update_client, name='update-client'),
    path('clients/', clients_views.ClientsListView.as_view(), name='clients')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
