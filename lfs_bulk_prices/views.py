"""Views: the bulk prices tab in the management interface and the price update for the product page."""

import json

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db import IntegrityError, transaction
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils.formats import sanitize_separators
from django.utils.translation import gettext_lazy as _
from django.views.generic import TemplateView

from lfs.catalog.models import Product
from lfs.core.templatetags.lfs_tags import currency
from lfs.manage.products.views import ProductTabMixin

from .models import BulkPrice


def _number(value: str | None, default: float) -> float:
    """Parse a number entered with a decimal comma or point; ``default`` if it is missing or invalid.

    The tab's JavaScript always writes a decimal comma, whatever the shop's language.
    """
    if value is None:
        return default
    try:
        return float(sanitize_separators(value).replace(",", "."))
    except (TypeError, ValueError):
        return default


class ProductBulkPricesView(PermissionRequiredMixin, ProductTabMixin, TemplateView):
    """The product's bulk prices tab: shows the price tiers and replaces them on POST."""

    tab_name = "bulk_prices"
    permission_required = "core.manage_shop"

    def get_context_data(self, **kwargs) -> dict:
        """Add the product's tiers, ordered by amount, and the currency."""
        ctx = super().get_context_data(**kwargs)
        ctx["prices"] = list(BulkPrice.objects.filter(product=self.get_product()).order_by("amount"))
        ctx["currency"] = getattr(settings, "LFS_CURRENCY", "EUR")
        return ctx

    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        """Replace all tiers of the product with the submitted ones; a tier repeating an amount or price is dropped."""
        product = self.get_product()
        BulkPrice.objects.filter(product=product).delete()

        duplicates = False
        for price_id in request.POST.getlist("price_id"):
            try:
                with transaction.atomic():
                    BulkPrice.objects.create(
                        product=product,
                        amount=_number(request.POST.get(f"amount-{price_id}"), 1.0),
                        price_absolute=_number(request.POST.get(f"price_absolute-{price_id}"), 0.0),
                        price_percentual=_number(request.POST.get(f"price_percentual-{price_id}"), 0.0),
                    )
            except IntegrityError:
                duplicates = True

        if duplicates:
            messages.info(request, _("Duplicated prices have been removed."))
        messages.success(request, _("Bulk prices have been saved."))
        return HttpResponseRedirect(reverse("lfs_manage_product_bulk_prices", kwargs={"id": product.pk}))


def update_prices(request: HttpRequest, product_id: int) -> HttpResponse:
    """Return the product's price and base price for GET ``amount`` as JSON, for the product page."""
    product = get_object_or_404(Product, pk=product_id)
    try:
        amount = int(request.GET.get("amount", 1))
    except (TypeError, ValueError):
        amount = 1

    result = json.dumps(
        {
            "standard_price": currency(product.get_price_gross(request, amount=amount), request) + "*",
            "base_price": currency(product.get_base_price_gross(request, amount=amount), request) + "*",
        }
    )
    return HttpResponse(result, content_type="application/json")
