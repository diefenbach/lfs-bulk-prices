from lfs.gross_price.calculator import GrossPriceCalculator
from . models import BulkPrice


class BulkPricesCalculator(GrossPriceCalculator):
    """
    """
    def get_price(self, with_properties=True, amount=1):
        """
        """
        if self.product.is_variant() and (self.product.price_calculator is None):
            product = self.product.get_parent()
        else:
            product = self.product

        for bulk_price in BulkPrice.objects.filter(product=product).order_by("-amount"):
            if amount >= bulk_price.amount:
                return bulk_price.price_absolute

        return 0.0
