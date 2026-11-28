"""The price calculator of the add-on: prices by the ordered amount."""

from lfs.gross_price.calculator import GrossPriceCalculator

from .models import BulkPrice


class BulkPricesCalculator(GrossPriceCalculator):
    """Gross prices from the product's tiers: the tier with the highest minimum quantity the amount reaches.

    A variant without tiers of its own uses those of its parent. Without a tier for the amount (none saved, or the
    first starts above it) the product's own price applies, as with the gross price calculator, instead of 0.
    """

    def get_price(self, with_properties: bool = True, amount: float = 1) -> float:
        """Return the price per unit for ``amount`` before taxes are calculated."""
        target_product = self.product
        if self.product.is_variant() and not BulkPrice.objects.filter(product=self.product).exists():
            target_product = self.product.get_parent()

        for bulk_price in BulkPrice.objects.filter(product=target_product).order_by("-amount"):
            if amount >= bulk_price.amount:
                return bulk_price.price_absolute

        return super().get_price(with_properties, amount)
