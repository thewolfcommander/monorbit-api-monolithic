from django.contrib import admin
from django.urls import path, include
from rest_framework_swagger.views import get_swagger_view


urlpatterns = [
    path('admin/', admin.site.urls),

    # API
    path('api/v1/accounts/', include('accounts.urls', namespace='accounts')),
    path('api/v1/addresses/', include('addresses.urls', namespace='addresses')),
    path('api/v1/adminer/', include('adminer.urls', namespace='adminer')),
    path('api/v1/cart/', include('cart.urls', namespace='cart')),
    path('api/v1/core/', include('core.urls', namespace='core')),
    path('api/v1/profiles/job/', include('job_profiles.urls', namespace='job_profiles')),
    path('api/v1/greivances/', include('greivances.urls', namespace='greivances')),
    path('api/v1/network/', include('network.urls', namespace='network')),
    path('api/v1/orders/', include('orders.urls', namespace='orders')),
    path('api/v1/premium/', include('premium.urls', namespace='premium')),
    path('api/v1/catalog/product/', include('product_catalog.urls', namespace='product')),
    path('api/v1/transactions/', include('transactions.urls', namespace='transactions')),
]
