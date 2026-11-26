"""URLs for the add-on's tests: the shop, the management interface, and the add-on."""

from django.urls import include, path

urlpatterns = [
    path("", include("lfs.core.urls")),
    path("manage/", include("lfs.manage.urls")),
    path("bulk-prices/", include("lfs_bulk_prices.urls")),
]
