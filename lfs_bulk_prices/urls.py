"""URLs of the add-on; a shop includes them under a prefix such as ``bulk-prices/``."""

from django.urls import path

from . import views

urlpatterns = [
    path("manage/product/<int:id>/", views.ProductBulkPricesView.as_view(), name="lfs_manage_product_bulk_prices"),
    path("update-prices/<int:product_id>", views.update_prices, name="lfs_bulk_prices_update_prices"),
]
