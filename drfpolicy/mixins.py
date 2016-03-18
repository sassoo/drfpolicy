"""
    drfpolicy.mixins
    ~~~~~~~~~~~~~~~~

    DRF policy module mixins for different DRF native objects.
"""

from .permissions import PolicyPermission
from django.utils.functional import cached_property


__all__ = ('PolicyViewMixin',)


class PolicyViewMixin(object):
    """ DRF policy mixin for DRF APIView & GenericAPIView

    This mixin will override the `get_queryset` &
    `get_serializer_class` methods to support a single
    source-of-truth when determining which serializer &
    queryset to use by consulting the policy object.

    This behavior can be short circuited by specificying the
    `queryset` & `serializer_class` on the view like you
    would normally do when following the DRF docs.
    """

    @cached_property
    def policy(self):
        """ Return the policy object instance """

        return self.get_policy()

    def get_permissions(self):
        """ Override DRF APIView """

        permissions = super(PolicyViewMixin, self).get_permissions()
        permissions.append(PolicyPermission())
        return permissions

    def get_policy(self):
        """ Return a policy instance from the `policy_class` property """

        policy = getattr(self, 'policy_class', None)
        if policy:
            policy = policy(self.request, self)
        return policy

    def get_serializer_class(self):
        """ Override DRF GenericAPIView """

        serializer_class = getattr(self, 'serializer_class', None)
        if not serializer_class:
            serializer_class = self.policy.get_serializer_class()
            setattr(self, 'serializer_class', serializer_class)
        return super(PolicyViewMixin, self).get_serializer_class()

    def perform_create(self, serializer):
        """ Call can_create_object with an already validated serializer

        An instance isn't available until the save has occurred
        so the `can_create_object` method is a bit unusual in
        this case.
        """

        self.policy.can_create_object(serializer)
        return super(PolicyViewMixin, self).perform_create(serializer)

    def perform_update(self, serializer):
        """ Call `can_update_object` with the validated instance """

        self.policy.can_update_object(serializer.instance, valid=True)
        return super(PolicyViewMixin, self).perform_update(serializer)
