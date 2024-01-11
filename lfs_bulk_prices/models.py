from django.db import models
from django.utils.translation import gettext_lazy as _
from lfs.catalog.models import Product


class BulkPrice(models.Model):
    """ """

    class Meta:
        ordering = ("amount",)
        unique_together = (
            ("product", "price_absolute"),
            ("product", "amount"),
        )

    product = models.ForeignKey(Product, verbose_name=_("Product"), on_delete=models.CASCADE)
    amount = models.FloatField(_("Amount"))
    price_absolute = models.FloatField(_("Price absolute"), default=0.0)
    price_percentual = models.FloatField(_("Price percentual"), default=0.0)
