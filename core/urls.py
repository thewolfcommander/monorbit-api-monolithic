from django.urls import path

from .views import *


app_name = "core"

urlpatterns = [
    path(
        "tips-to-grow/", ListCreateTipToGrow.as_view(), name="list_create_tips_to_grow"
    ),
    path("tips-to-grow/random/", GetARandomTip.as_view(), name="get_a_random_tip"),
    path(
        "tips-to-grow/update/<int:id>/",
        UpdateTipToGrow.as_view(),
        name="update_tips_to_grow",
    ),
    path("email/send/", SendEmail.as_view(), name="send_email"),
    path("email/all/", AllEmail.as_view(), name="all_email"),
    path(
        "user/devices/",
        ListCreateUserDeviceRegistration.as_view(),
        name="list_create_user_devices",
    ),
    path(
        "user/devices/update/<slug:id>/",
        UpdateUserDeviceRegistration.as_view(),
        name="update_user_devices",
    ),
    path(
        "user/activity/auth/",
        ListCreateUserLoginActivity.as_view(),
        name="list_create_user_login_activity",
    ),
    path(
        "user/activity/auth/<int:id>/",
        UpdateUserLoginActivity.as_view(),
        name="update_user_login_activity",
    ),

    path("handler/file/upload/", FileUploadView.as_view(), name="upload_file"),
    # path("handler/file/upload/test/", FileView.as_view(), name="upload_file2"),
    path(
        "handler/network/orders/", ListAllNetworkOrders.as_view(), name="network_orders"
    ),
    path('handler/products/search/', ProductsSearch.as_view(), name='products_search'),
    path('handler/networks/search/', NetworkSearch.as_view(), name='networks_search'),
    path('handler/orders/search/', OrderSearch.as_view(), name='orders_search'),
]
