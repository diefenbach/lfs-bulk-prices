import locale
from django import template
from django.db.models import F
from django.db.models import Min
from django.utils.safestring import mark_safe
from django.template import Library
from django.template import RequestContext
from django.template.loader import render_to_string
import lfs.core.views
from .. models import BulkPrice
register = Library()


@register.simple_tag(takes_context=True)
def bulk_prices_management(context, product):
    request = context.get("request")
    prices = BulkPrice.objects.filter(product=product)

    if locale.getlocale(locale.LC_ALL)[0] is None:
        lfs.core.views.one_time_setup()

    result = render_to_string("lfs_bulk_prices/lfs_bulk_prices.html", RequestContext(request, {
        "product": product,
        "prices": prices,
        "currency": locale.localeconv()["int_curr_symbol"],
    }))

    return mark_safe(result)


class IfBulkPricesNode(template.Node):
    @classmethod
    def handle_token(cls, parser, token):
        bits = token.contents.split()
        if len(bits) != 1:
            raise template.TemplateSyntaxError(
                "'%s' tag takes one argument" % bits[0])
        end_tag = 'endifbulkprices'
        nodelist_true = parser.parse(('else', end_tag))
        token = parser.next_token()
        if token.contents == 'else':  # there is an 'else' clause in the tag
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
        if product.is_variant() and product.price_calculator is None:
            product = product.get_parent()

        context["bulk_prices"] = BulkPrice.objects.filter(product=product).annotate(price_percentual_discount=100 - F("price_percentual"))
        context["bulk_prices_min"] = BulkPrice.objects.filter(product=product).aggregate(Min('price_absolute'))["price_absolute__min"]
        return ''


@register.tag('bulk_prices')
def bulk_prices(parser, token):
    return BulkPricesNode()
