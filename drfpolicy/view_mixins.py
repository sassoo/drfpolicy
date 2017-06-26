"""
    drfpolicy.view_mixins
    ~~~~~~~~~~~~~~~~~~~~~

    DRF policy module mixins for different DRF native objects.
"""


class PolicyModelMixin:
    """ DRF policy mixin for DRF ModelViewSet

    For DRF ModelViewSet mixins this will override the native
    perform_create & update methods to call the appropriate
    permission object check handlers post validation.
    """

    def perform_create(self, serializer):
        """ DRF override

        An instance isn't available until the save has occurred
        so the permission hooks for creation are a bit unusual in
        this case by passing in the serializer only.
        """

        for perm in self.get_permissions():
            try:
                perm.can_create_valid_object(self.request, self, serializer)
            except AttributeError:
                continue

        return super().perform_create(serializer)

    def perform_update(self, serializer):
        """ DRF override

        The already validated & "dirty" object is passed to the
        method amongst the default request & view.
        """

        obj = serializer.instance
        for perm in self.get_permissions():
            try:
                perm.can_update_valid_object(self.request, self, obj)
            except AttributeError:
                continue

        return super().perform_update(serializer)
