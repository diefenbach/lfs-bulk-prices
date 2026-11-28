"""Signal listeners of the add-on."""

import logging

from lfs.order.models import Order

from .calculator import BulkPricesCalculator, tier_for

logger = logging.getLogger("lfs_bulk_prices")


def warn_about_items_without_tier(sender: Order, **kwargs: object) -> None:
    """Log a warning for every item of the new order whose bulk-priced product had no tier for its amount.

    Such an item was charged at the product's own price; the warning shows that the product's tiers need care.
    """
    for item in sender.items.select_related("product"):
        product = item.product
        if product is None or not isinstance(product.get_price_calculator(None), BulkPricesCalculator):
            continue
        if tier_for(product, item.product_amount) is None:
            logger.warning(
                "Order %s: product %s (%s) has no price tier for the amount %s; charged its own price",
                sender.number,
                product.slug,
                product.id,
                item.product_amount,
            )
