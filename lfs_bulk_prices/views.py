from django.db import IntegrityError
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from . models import BulkPrice


def lfs_bulk_prices_update(request):
    """
    """

    product_id = request.POST.get("product_id")

    if request.method == "POST":

        # 1st delete all bulk prices for the product
        BulkPrice.objects.filter(product_id=product_id).delete()

        # 2nd add bulk prices again
        for price_id in request.POST.getlist("price_id"):
            try:
                amount = int(request.POST.get("amount-{}".format(price_id)))
            except (TypeError, ValueError):
                amount = 1
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
                pass

    return redirect(reverse("lfs_manage_product", kwargs={"product_id": product_id}))
