from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from apps.catalogs import views as catalog_views
from apps.main import views as main_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('settings/', main_views.SettingsViews.as_view(), name='settings'),
    path('products/', catalog_views.PriceListViews.as_view(), name='products'),
    path('product/<int:product_id>/profile/<int:profile_id>/', catalog_views.ProductProfileViews.as_view(), name='product-profile'),
    path('product/<int:product_id>/profile/add/', catalog_views.ProductProfileAdd.as_view(), name='product-profile-add'),
    path('product/<int:product_id>/profile/<int:profile_id>/size/add/', catalog_views.add_size_to_profile, name='add-size-to-profile'),
    path('', main_views.HomePageViews.as_view(), name='home-page'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)