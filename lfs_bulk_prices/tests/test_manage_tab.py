"""The add-on's tab on the product management page: listed only for products with the bulk prices calculator,
and saving it stores the price tiers."""

import pytest
from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.urls import reverse

from lfs.catalog.models import Product
from lfs_bulk_prices.models import BulkPrice

BULK = "lfs_bulk_prices.calculator.BulkPricesCalculator"
GROSS = "lfs.gross_price.calculator.GrossPriceCalculator"


@pytest.fixture
def admin_client(client, db):
    call_command("lfs_init")
    client.force_login(get_user_model().objects.create_superuser("admin", "admin@example.com", "x"))
    return client


def make_product(calculator: str) -> Product:
    return Product.objects.create(name="Board", slug="board", sku="B1", price=10, active=True, price_calculator=calculator)


def test_tab_is_listed_for_products_with_bulk_prices(admin_client):
    product = make_product(BULK)

    content = admin_client.get(reverse("lfs_manage_product_data", args=[product.pk])).content.decode()

    assert reverse("lfs_manage_product_bulk_prices", args=[product.pk]) in content


def test_tab_is_not_listed_for_other_products(admin_client):
    product = make_product(GROSS)

    content = admin_client.get(reverse("lfs_manage_product_data", args=[product.pk])).content.decode()

    assert reverse("lfs_manage_product_bulk_prices", args=[product.pk]) not in content


def test_tab_shows_the_stored_tiers(admin_client):
    product = make_product(BULK)
    BulkPrice.objects.create(product=product, amount=10, price_absolute=8.5, price_percentual=85)

    content = admin_client.get(reverse("lfs_manage_product_bulk_prices", args=[product.pk])).content.decode()

    assert 'id="bulk-prices-form"' in content
    assert 'value="8.5"' in content


def test_saving_replaces_the_tiers(admin_client):
    product = make_product(BULK)
    BulkPrice.objects.create(product=product, amount=5, price_absolute=9, price_percentual=90)

    response = admin_client.post(
        reverse("lfs_manage_product_bulk_prices", args=[product.pk]),
        {
            "price_id": ["first", "2"],
            "amount-first": "1",
            "price_absolute-first": "10",
            "price_percentual-first": "100",
            "amount-2": "10,0",
            "price_absolute-2": "8,5",
            "price_percentual-2": "85",
        },
    )

    assert response.status_code == 302
    assert list(BulkPrice.objects.filter(product=product).values_list("amount", "price_absolute")) == [
        (1.0, 10.0),
        (10.0, 8.5),
    ]


def test_calculator_uses_the_tier_for_the_amount(admin_client, rf):
    product = make_product(BULK)
    BulkPrice.objects.create(product=product, amount=1, price_absolute=10, price_percentual=100)
    BulkPrice.objects.create(product=product, amount=10, price_absolute=8.5, price_percentual=85)
    request = rf.get("/")

    assert product.get_price(request, amount=9) == 10
    assert product.get_price(request, amount=10) == 8.5


def test_saving_drops_a_repeated_amount_and_keeps_the_rest(admin_client):
    product = make_product(BULK)

    response = admin_client.post(
        reverse("lfs_manage_product_bulk_prices", args=[product.pk]),
        {
            "price_id": ["first", "2", "3"],
            "amount-first": "1",
            "price_absolute-first": "10",
            "amount-2": "10",
            "price_absolute-2": "9",
            "amount-3": "10",
            "price_absolute-3": "8",
        },
    )

    assert response.status_code == 302
    assert list(BulkPrice.objects.filter(product=product).values_list("amount", flat=True)) == [1.0, 10.0]


def test_tab_says_when_no_tiers_are_saved_yet(admin_client):
    """The tab pre-fills a base price row for a product without tiers; it must not look saved (Höhne, 28.11.2026)."""
    product = make_product(BULK)
    url = reverse("lfs_manage_product_bulk_prices", args=[product.pk])

    assert "No price tiers saved yet" in admin_client.get(url).content.decode()

    BulkPrice.objects.create(product=product, amount=1, price_absolute=10)
    assert "No price tiers saved yet" not in admin_client.get(url).content.decode()
