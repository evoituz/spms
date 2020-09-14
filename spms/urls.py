from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from apps.catalogs.views import *
from apps.main.views import SettingsViews

urlpatterns = [
    path('admin/', admin.site.urls),
    path('settings/', SettingsViews.as_view(), name='settings'),
    path('products/', PriceListViews.as_view(), name='products'),
    path('product/<int:product_id>/profile/<int:profile_id>/', ProductProfileViews.as_view(), name='product-profile'),
    path('catalogs/product/<int:product_id>/profile/add/', ProductProfileAdd.as_view(), name='product-profile-add'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)