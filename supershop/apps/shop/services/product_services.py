from ..models import Product


class MinResolutionException(Exception):
    pass


class MaxResolutionException(Exception):
    pass


class MaxImageFileSizeException(Exception):
    pass


def get_to_sell_products():
    return Product.objects.filter(to_sell=True)
