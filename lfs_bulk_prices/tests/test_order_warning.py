"""An order with a bulk-priced product that reached no price tier is logged, so that missing tiers get noticed."""

import logging

import pytest
from django.contrib.contenttypes.models import ContentType
from django.core.management import call_command

from lfs.addresses.models import Address
from lfs.catalog.models import Product
from lfs.core.models import Country
from lfs.core.signals import order_created
from lfs.order.models import Order, OrderItem
from lfs_bulk_prices.models import BulkPrice

BULK = "lfs_bulk_prices.calculator.BulkPricesCalculator"


@pytest.fixture
def order(db):
    call_command("lfs_init")
    address = Address.objects.create(
        firstname="A", lastname="B", line1="x", city="y", zip_code="1", country=Country.objects.first(), email="a@b.c"
    )
    content_type = ContentType.objects.get_for_model(Address)
    return Order.objects.create(
        number="1", price=10, tax=1, customer_email="a@b.c", sa_content_type=content_type, sa_object_id=address.id,
        ia_content_type=content_type, ia_object_id=address.id,
    )


def add_item(order: Order, product: Product, amount: float) -> None:
    OrderItem.objects.create(
        order=order, product=product, product_name=product.name, product_amount=amount, product_price_gross=10,
        price_gross=10 * amount,
    )


def test_order_with_a_product_without_tier_logs_a_warning(order, caplog):
    product = Product.objects.create(name="Board", slug="board", sku="B1", price=37.88, price_calculator=BULK)
    BulkPrice.objects.create(product=product, amount=10, price_absolute=33.5)
    add_item(order, product, 2)

    with caplog.at_level(logging.WARNING, logger="lfs_bulk_prices"):
        order_created.send(order, cart=None, request=None)

    assert "no price tier" in caplog.text
    assert "board" in caplog.text


def test_order_within_the_tiers_logs_nothing(order, caplog):
    product = Product.objects.create(name="Board", slug="board", sku="B1", price=37.88, price_calculator=BULK)
    BulkPrice.objects.create(product=product, amount=1, price_absolute=37.88)
    add_item(order, product, 2)

    with caplog.at_level(logging.WARNING, logger="lfs_bulk_prices"):
        order_created.send(order, cart=None, request=None)

    assert "no price tier" not in caplog.text
