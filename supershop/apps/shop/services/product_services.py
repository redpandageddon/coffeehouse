from django.urls import reverse

class MinResolutionException(Exception):
    pass


class MaxResolutionException(Exception):
    pass

class MaxImageFileSizeException(Exception):
    pass