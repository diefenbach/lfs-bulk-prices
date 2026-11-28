"""The bulk prices calculator: the tier the ordered amount reaches, otherwise the product's own price.

A product whose tiers were never saved (or start above the ordered amount) used to cost 0 in the shop; the Höhne shops
sold seven products for 0 € that way (28.11.2026).
"""

import pytest
from django.test import RequestFactory

from lfs.catalog.models import Product
from lfs.catalog.settings import PRODUCT_WITH_VARIANTS, VARIANT
from lfs_bulk_prices.models import BulkPrice

BULK = "lfs_bulk_prices.calculator.BulkPricesCalculator"


@pytest.fixture
def request_(db):
    request = RequestFactory().get("/")
    request.user = None
    return request


def make_product(**kwargs) -> Product:
    defaults = {"name": "Board", "slug": "board", "sku": "B1", "price": 37.88, "active": True, "price_calculator": BULK}
    return Product.objects.create(**{**defaults, **kwargs})


def test_amount_reaching_a_tier_gets_the_tier_price(request_):
    product = make_product()
    BulkPrice.objects.create(product=product, amount=1, price_absolute=37.88)
    BulkPrice.objects.create(product=product, amount=10, price_absolute=33.50)

    assert product.get_price(request_, amount=1) == 37.88
    assert product.get_price(request_, amount=10) == 33.50
    assert product.get_price(request_, amount=25) == 33.50


def test_product_without_saved_tiers_costs_its_own_price(request_):
    product = make_product()

    assert product.get_price(request_, amount=1) == 37.88


def test_amount_below_the_first_tier_costs_the_product_price(request_):
    product = make_product()
    BulkPrice.objects.create(product=product, amount=10, price_absolute=33.50)

    assert product.get_price(request_, amount=1) == 37.88
    assert product.get_price(request_, amount=10) == 33.50


def test_variant_without_tiers_of_its_own_or_its_parent_costs_its_own_price(request_):
    parent = make_product(sub_type=PRODUCT_WITH_VARIANTS)
    variant = make_product(
        name="Board 4.2 m", slug="board-420", sku="B1-420", price=47.21, sub_type=VARIANT, parent=parent,
        active_price=True, price_calculator="",
    )

    assert variant.get_price(request_, amount=1) == 47.21
