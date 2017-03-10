from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.lfs_bulk_prices_update, name="lfs_bulk_prices_update"),
    url(r'^update-prices/(?P<product_id>\d*)$', views.update_prices, name="lfs_bulk_prices_update_prices"),
]
