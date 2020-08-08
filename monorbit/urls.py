from django.contrib import admin
from django.urls import path, include
from rest_framework_swagger.views import get_swagger_view


urlpatterns = [
    path('admin/', admin.site.urls),

    # API
    path('api/v1/accounts/', include('accounts.urls')),
]
