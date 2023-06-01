from django_filters.rest_framework import FilterSet
from . import models


class ItemFilter(FilterSet):
    class Meta:
        model = models.Item
        fields = {
            'type': ['exact'],
            'brand': ['exact'],
            'material': ['exact'],
            'occasion': ['exact'],
        }


class CrawledItemFilter(ItemFilter):
    class Meta:
        model = models.CrawledItem
        fields = {'price': ['gt', 'lt'], **ItemFilter.Meta.fields}


class OwnedItemFilter(ItemFilter):
    class Meta:
        model = models.OwnedItem
        fields = {'is_public': ['exact'], **ItemFilter.Meta.fields}
