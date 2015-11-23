from django.conf.urls import patterns, url

urlpatterns = patterns('django.contrib.auth.views',
    url('^login', "login", {"template_name": "lfs_bulk_prices/login.html"}, name='lfs_bulk_prices_login'),
    url('^logout', "logout", {"template_name": "lfs_bulk_prices/logged_out.html"}, name='lfs_bulk_prices_logout'),
)

urlpatterns += patterns('lfs_bulk_prices.views',
    url(r'^$', "lfs_bulk_prices_update", name="lfs_bulk_prices_update"),
)
