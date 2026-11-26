# lfs-bulk-prices

Bulk prices for [LFS](https://github.com/diefenbach/django-lfs): price tiers by quantity ("from 10 pieces 8.50 €").

- A price calculator, `BulkPricesCalculator`, that picks the tier for the ordered amount.
- A **Bulk prices** tab on the product management page, shown for products that use this calculator.
- Template tags and a small script for the product page that show the tiers and update the price when the
  customer changes the amount. lfs-theme includes them when the add-on is installed.

## Installation

```sh
pip install lfs-bulk-prices        # or, in lfs-project: uv sync --extra bulk-prices
```

```python
# settings.py
INSTALLED_APPS = [..., "lfs_bulk_prices"]

LFS_PRICE_CALCULATORS = [
    ["lfs.gross_price.calculator.GrossPriceCalculator", _("Price includes tax")],
    ["lfs.net_price.calculator.NetPriceCalculator", _("Price excludes tax")],
    ["lfs_bulk_prices.calculator.BulkPricesCalculator", _("Bulk prices")],
]

# urls.py
urlpatterns += [path("bulk-prices/", include("lfs_bulk_prices.urls"))]
```

Then run `python manage.py migrate`. In the management interface choose the price calculator "Bulk prices" for a
product (or for the shop as default); the product then gets the **Bulk prices** tab.

## Tests

```sh
pytest
```

The tests use `lfs_bulk_prices.tests.settings` and need django-lfs with its required add-ons installed.

## License

BSD-3-Clause, see `LICENSE.txt`.
