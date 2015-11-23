# django imports
from django.utils.safestring import mark_safe
from django import template
from django.template import Library
from django.template import RequestContext
from django.template.loader import render_to_string
from .. models import BulkPrice
register = Library()


@register.simple_tag(takes_context=True)
def bulk_prices_management(context, product):
    request = context.get("request")
    prices = BulkPrice.objects.filter(product=product)
    result = render_to_string("lfs_bulk_prices/lfs_bulk_prices.html", RequestContext(request, {
        "product": product,
        "prices": prices,
    }))

    return mark_safe(result)


class GetPriceCalculatorNode(template.Node):
    """
    """
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
        if product.get_price_calculator(request).__class__.__name__ == "BulkPricesCalculator":
            return self.nodelist_true.render(context)
        else:
            return self.nodelist_false


@register.tag
def ifbulkprices(parser, token):
    """This function provides functionality for the 'ifbulkprices' template tag.
    """
    return GetPriceCalculatorNode.handle_token(parser, token)
