"""App configuration: registers the bulk prices tab and the order listener."""

from django.apps import AppConfig
from django.http import HttpRequest
from django.utils.translation import gettext_lazy as _


def uses_bulk_prices(request: HttpRequest, product) -> bool:
    """Return whether ``product`` is priced with the bulk prices calculator (its own or its parent's)."""
    from .calculator import BulkPricesCalculator

    return isinstance(product.get_price_calculator(request), BulkPricesCalculator)


class LfsBulkPricesConfig(AppConfig):
    """Adds the "Bulk prices" tab to products that use the bulk prices calculator and logs orders without a tier."""

    name = "lfs_bulk_prices"
    verbose_name = _("Bulk prices")

    def ready(self) -> None:
        """Register the product tab and the warning about order items without a price tier."""
        from lfs.core.signals import order_created
        from lfs.manage.products.tabs import ProductTab, register_product_tab

        from .listeners import warn_about_items_without_tier

        order_created.connect(warn_about_items_without_tier, dispatch_uid="lfs_bulk_prices_items_without_tier")

        register_product_tab(
            ProductTab(
                key="bulk_prices",
                label=_("Bulk prices"),
                url_name="lfs_manage_product_bulk_prices",
                template="lfs_bulk_prices/manage/tab.html",
                show=uses_bulk_prices,
            )
        )
