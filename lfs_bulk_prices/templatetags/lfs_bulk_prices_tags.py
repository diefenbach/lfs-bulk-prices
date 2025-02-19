import sys

from django import template
from django.conf import settings
from django.db.models import F
from django.db.models import Min
from django.utils.safestring import mark_safe
from django.template import Library
from django.template.loader import render_to_string

from lfs.catalog.models import Product
from lfs.catalog.settings import CATEGORY_VARIANT_CHEAPEST_PRICES
from lfs_bulk_prices.models import BulkPrice

register = Library()


@register.simple_tag(takes_context=True)
def bulk_prices_management(context, product):
    request = context.get("request")
    prices = BulkPrice.objects.filter(product=product)

    result = render_to_string(
        "lfs_bulk_prices/lfs_bulk_prices.html",
        request=request,
        context={
            "product": product,
            "prices": prices,
            "currency": getattr(settings, "LFS_CURRENCY", "EUR"),
        },
    )

    return mark_safe(result)


class IfBulkPricesNode(template.Node):
    @classmethod
    def handle_token(cls, parser, token):
        bits = token.contents.split()
        if len(bits) != 1:
            raise template.TemplateSyntaxError("'%s' tag takes one argument" % bits[0])
        end_tag = "endifbulkprices"
        nodelist_true = parser.parse(("else", end_tag))
        token = parser.next_token()
        if token.contents == "else":  # there is an 'else' clause in the tag
            nodelist_false = parser.parse((end_tag,))
            parser.delete_first_token()
        else:
            nodelist_false = ""

        return cls(bits[0], nodelist_true, nodelist_false)

    def __init__(self, codename, nodelist_true, nodelist_false):
        self.codename = codename
        self.nodelist_true = nodelist_true
        self.nodelist_false = nodelist_false

    def render(self, context):
        product = context.get("product")
        request = context.get("request")

        if product.is_variant():
            if product.price_calculator == "lfs_bulk_prices.calculator.BulkPricesCalculator":
                return self.nodelist_true.render(context)
            elif product.price_calculator is None:
                product = product.get_parent()

        if product.get_price_calculator(request).__class__.__name__ == "BulkPricesCalculator":
            return self.nodelist_true.render(context)

        return self.nodelist_false


@register.tag
def ifbulkprices(parser, token):
    return IfBulkPricesNode.handle_token(parser, token)


class BulkPricesNode(template.Node):
    def render(self, context):
        product = context["product"]
        request = context["request"]
        if product.is_variant() and product.price_calculator is None:
            product = product.get_parent()

        bulk_prices = []
        for bulk_price in BulkPrice.objects.filter(product=product).annotate(
            price_percentual_discount=100 - F("price_percentual")
        ):
            bulk_price.base_price = product.get_base_price_gross(request, amount=bulk_price.amount)
            bulk_prices.append(bulk_price)
        context["bulk_prices"] = bulk_prices
        context["bulk_prices_min"] = BulkPrice.objects.filter(product=product).aggregate(Min("price_absolute"))[
            "price_absolute__min"
        ]
        return ""


@register.tag("bulk_prices")
def bulk_prices(parser, token):
    return BulkPricesNode()


class CategoryProductPricesGrossNode(template.Node):
    def __init__(self, product_id):
        self.product_id = template.Variable(product_id)

    def render(self, context):
        request = context.get("request")

        product_id = self.product_id.resolve(context)
        product = Product.objects.get(pk=product_id)

        if product.is_variant():
            parent = product.parent
        else:
            parent = product

        if parent.category_variant == CATEGORY_VARIANT_CHEAPEST_PRICES:
            if product.get_for_sale():
                info = parent.get_cheapest_standard_price_gross(request)
                context["standard_price"] = info["price"]
                context["standard_price_starting_from"] = info["starting_from"]

            info = parent.get_cheapest_price_gross(request)
            context["price"] = info["price"]
            context["price_starting_from"] = info["starting_from"]

            info = parent.get_cheapest_base_price_gross(request)
            context["base_price"] = info["price"]
            context["base_price_starting_from"] = info["starting_from"]

            if product.get_active_packing_unit():
                context["base_packing_price"] = product.get_base_packing_price_gross(request, amount=sys.maxsize)
                context["base_packing_price_starting_from"] = info["starting_from"]
        else:
            if product.get_price_calculator(request).__class__.__name__ == "BulkPricesCalculator":
                starting_from = True
            else:
                starting_from = False

            if product.get_for_sale():
                context["standard_price"] = product.get_standard_price_gross(request, amount=sys.maxsize)

            context["price"] = product.get_price_gross(request, amount=sys.maxsize)
            context["price_starting_from"] = starting_from

            context["base_price"] = product.get_base_price_gross(request, amount=sys.maxsize)
            context["base_price_starting_from"] = starting_from

            if product.get_active_packing_unit():
                context["base_packing_price"] = product.get_base_packing_price_gross(request, amount=sys.maxsize)
                context["base_packing_price_starting_from"] = starting_from

        return ""


@register.tag("bulk_prices_category_product_prices_gross")
def bulk_prices_category_product_prices_gross(parser, token):
    """
    Injects all needed gross prices for the default category products view into
    the context.
    """
    bits = token.contents.split()
    return CategoryProductPricesGrossNode(bits[1])


@register.filter(name="get_cheapest_price")
def get_cheapest_price(product, request):
    return product.get_price(request, amount=sys.maxsize)


@register.filter(name="get_cheapest_price_net")
def get_cheapest_price_net(product, request):
    return product.get_price_net(request, amount=sys.maxsize)


@register.filter(name="get_cheapest_price_gross")
def get_cheapest_price_gross(product, request):
    return product.get_price_gross(request, amount=sys.maxsize)


@register.filter(name="get_cheapest_standard_price")
def get_cheapest_standard_price(product, request):
    return product.get_standard_price(request, amount=sys.maxsize)


@register.filter(name="get_cheapest_standard_price_net")
def get_cheapest_standard_price_net(product, request):
    return product.get_standard_price_net(request, amount=sys.maxsize)


@register.filter(name="get_cheapest_standard_price_gross")
def get_cheapest_standard_price_gross(product, request):
    return product.get_standard_price_gross(request, amount=sys.maxsize)


@register.filter(name="get_cheapest_for_sale_price")
def get_cheapest_for_sale_price(product, request):
    return product.get_for_sale_price(request, amount=sys.maxsize)


@register.filter(name="get_cheapest_for_sale_price_net")
def get_cheapest_for_sale_price_net(product, request):
    return product.get_for_sale_price_net(request, amount=sys.maxsize)


@register.filter(name="get_cheapest_for_sale_price_gross")
def get_cheapest_for_sale_price_gross(product, request):
    return product.get_for_sale_price_gross(request, amount=sys.maxsize)


@register.filter(name="get_cheapest_base_price")
def get_cheapest_base_price(product, request):
    return product.get_base_price(request, amount=sys.maxsize)


@register.filter(name="get_cheapest_base_price_net")
def get_cheapest_base_price_net(product, request):
    return product.get_base_price_net(request, amount=sys.maxsize)


@register.filter(name="get_cheapest_base_price_gross")
def get_cheapest_base_price_gross(product, request):
    return product.get_base_price_gross(request, amount=sys.maxsize)


@register.filter(name="get_cheapest_base_packing_price")
def get_cheapest_base_packing_price(product, request):
    return product.get_base_packing_price(request, amount=sys.maxsize)


@register.filter(name="get_cheapest_base_packing_price_net")
def get_cheapest_base_packing_price_net(product, request):
    return product.get_base_packing_price_net(request, amount=sys.maxsize)


@register.filter(name="get_cheapest_base_packing_price_gross")
def get_cheapest_base_packing_price_gross(product, request):
    return product.get_base_packing_price_gross(request, amount=sys.maxsize)
