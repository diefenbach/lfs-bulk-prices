"""The price calculator of the add-on: prices by the ordered amount."""

from lfs.catalog.models import Product
from lfs.gross_price.calculator import GrossPriceCalculator

from .models import BulkPrice


def tier_for(product: Product, amount: float) -> BulkPrice | None:
    """Return the tier that applies to ``amount`` of ``product``, or None if the amount reaches none.

    The tier with the highest minimum quantity that ``amount`` reaches applies. A variant without tiers of its own
    uses those of its parent.
    """
    target_product = product
    if product.is_variant() and not BulkPrice.objects.filter(product=product).exists():
        target_product = product.get_parent()
    return BulkPrice.objects.filter(product=target_product, amount__lte=amount).order_by("-amount").first()


class BulkPricesCalculator(GrossPriceCalculator):
    """Gross prices from the product's tiers (see ``tier_for``).

    Without a tier for the amount (none saved, or the first starts above it) the product's own price applies, as with
    the gross price calculator, instead of 0; ``listeners`` logs orders where that happened.
    """

    def get_price(self, with_properties: bool = True, amount: float = 1) -> float:
        """Return the price per unit for ``amount`` before taxes are calculated."""
        tier = tier_for(self.product, amount)
        if tier is not None:
            return tier.price_absolute
        return super().get_price(with_properties, amount)
