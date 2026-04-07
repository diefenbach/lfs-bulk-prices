from lfs.gross_price.calculator import GrossPriceCalculator
from .models import BulkPrice


class BulkPricesCalculator(GrossPriceCalculator):
    """ """

    def get_price(self, with_properties=True, amount=1):
        """ """
        # If a variant has no price calculator the price calculator from the parent is used.
        # See also product.get_price_calculator().
        #
        # Once we are here, we have to check which bulk prices are applicable.
        # That means, if a variant has no bulk prices at all, the bulk prices from the parent are used.

        # First, determine the relevant product (use parent for variants if necessary)
        target_product = self.product
        if self.product.is_variant() and not BulkPrice.objects.filter(product=self.product).exists():
            target_product = self.product.get_parent()

        for bulk_price in BulkPrice.objects.filter(product=target_product).order_by("-amount"):
            if amount >= bulk_price.amount:
                return bulk_price.price_absolute

        return 0.0
