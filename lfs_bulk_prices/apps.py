"""App configuration: registers the bulk prices tab on the product management page."""

from django.apps import AppConfig
from django.http import HttpRequest
from django.utils.translation import gettext_lazy as _


def uses_bulk_prices(request: HttpRequest, product) -> bool:
    """Return whether ``product`` is priced with the bulk prices calculator (its own or its parent's)."""
    from .calculator import BulkPricesCalculator

    return isinstance(product.get_price_calculator(request), BulkPricesCalculator)


class LfsBulkPricesConfig(AppConfig):
    """Adds the "Bulk prices" tab to products that use the bulk prices calculator."""

    name = "lfs_bulk_prices"
    verbose_name = _("Bulk prices")

    def ready(self) -> None:
        """Register the product tab."""
        from lfs.manage.products.tabs import ProductTab, register_product_tab

        register_product_tab(
            ProductTab(
                key="bulk_prices",
                label=_("Bulk prices"),
                url_name="lfs_manage_product_bulk_prices",
                template="lfs_bulk_prices/manage/tab.html",
                show=uses_bulk_prices,
            )
        )
