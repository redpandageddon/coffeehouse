from os import name
from django.db import models


def get_models_for_count(*model_names):
    return [models.Count(model_name) for model_name in model_names]


class CategoryManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset()

    def get_categories_for_sidebar(self):
        models = get_models_for_count('product')
        query_set = list(self.get_queryset().annotate(*models))
        data = [
            dict(name = c.name, url = c.get_absolute_url(), count = c.product__count) for c in query_set
        ]
        return data