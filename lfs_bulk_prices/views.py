import json
from django.core.urlresolvers import reverse
from django.db import IntegrityError
from django.http import HttpResponse
from django.shortcuts import redirect
from django.utils.translation import ugettext_lazy as _
from lfs.catalog.models import Product
from lfs.core.templatetags.lfs_tags import currency
from lfs.core.utils import set_message_to
from . models import BulkPrice


def lfs_bulk_prices_update(request):
    """
    """
    product_id = request.POST.get("product_id")

    if request.method == "POST":
        # 1st delete all bulk prices for the product
        BulkPrice.objects.filter(product_id=product_id).delete()

        # 2nd add bulk prices again
        message = None
        for price_id in request.POST.getlist("price_id"):
            try:
                amount = float(request.POST.get("amount-{}".format(price_id)))
            except (TypeError, ValueError):
                amount = 1.0

            try:
                price_absolute = float(request.POST.get("price_absolute-{}".format(price_id)))
            except (TypeError, ValueError):
                price_absolute = 0.0

            try:
                price_percentual = float(request.POST.get("price_percentual-{}".format(price_id)))
            except (TypeError, ValueError):
                price_percentual = 0.0

            try:
                BulkPrice.objects.create(
                    product_id=product_id,
                    amount=amount,
                    price_absolute=price_absolute,
                    price_percentual=price_percentual,
                )
            except IntegrityError:
                message = _(u"Duplicated prices have been removed.")

    response = redirect(reverse("lfs_manage_product", kwargs={"product_id": product_id}))
    if message:
        set_message_to(response, message)
    return response


def update_prices(request, product_id):
    product = Product.objects.get(pk=product_id)
    try:
        amount = int(request.GET.get("amount", 1))
    except (TypeError, ValueError):
        amount = 1

    price = product.get_price_gross(request, amount=amount)
    base_price = product.get_base_price_gross(request, amount=amount)

    result = json.dumps({
        "standard_price": currency(price, request),
        "base_price": currency(base_price, request),
    })
    return HttpResponse(result, content_type='application/json')
