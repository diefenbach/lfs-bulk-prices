from django.urls import re_path
from . import views

urlpatterns = [
    re_path(r"^$", views.lfs_bulk_prices_update, name="lfs_bulk_prices_update"),
    re_path(r"^update-prices/(?P<product_id>\d*)$", views.update_prices, name="lfs_bulk_prices_update_prices"),
]
