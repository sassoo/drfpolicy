"""
    drfpolicy.filters
    ~~~~~~~~~~~~~~~~~

    DRF filter_backend to enforce a filtered queryset for
    security reasons. Supports a single source-of-truth
    for the information to keep things DRY.
"""

from django.core.exceptions import ImproperlyConfigured
from rest_framework.filters import BaseFilterBackend


__all__ = ('PolicyFilter',)


class PolicyFilter(BaseFilterBackend):
    """ Support the filtering of arbitrary resource fields """

    def filter_queryset(self, request, queryset, view):
        """ DRF entry point override into the custom FilterBackend """

        try:
            policy = view.policy
        except AttributeError:
            msg = 'Using "%s" requires a view that returns a policy ' \
                  'from the "policy" property. Make sure you inherited ' \
                  'from policy mixin in your ViewSet.'
            raise ImproperlyConfigured(msg % self.__class__.__name__)

        # the view is using the policy mixin but
        # has no policy. That's fine.
        if policy:
            filters = policy.filter_queryset(queryset)
            queryset = queryset.filter(*filters)

        return queryset
