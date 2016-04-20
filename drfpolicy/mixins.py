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

    This mixin will override the native `get_permissions`
    method to automatically include the PolicyPermission
    object to the existing list of permissions classes. It
    will then call the view's policy object authorization
    hooks.

    For GenericAPIView's the native perform_create & update
    methods will call the appropriate policy check handlers
    post validation. This means the object is technically
    "dirty" but validated. The `can_create_object` &
    `can_update_object` policy methods will be called with a
    kwargs containing {'validated': True} key/val pairs.
    """

    policy_class = None

    @cached_property
    def policy(self):
        """ Return the cached policy object instance

        This can & should be used when accessing the policy.
        It's less typing than `get_policy` & more efficient.
        """

        return self.get_policy()

    def get_permissions(self):
        """ Override DRF APIView

        Force the addition of the PolicyPermission object
        into the views permissions array. It should always
        be called.
        """

        permissions = super(PolicyViewMixin, self).get_permissions()
        permissions.append(PolicyPermission())
        return permissions

    def get_policy(self):
        """ Return a policy instance from the `policy_class` property """

        assert self.policy_class is not None, (
            '"%s" should either include a `policy_class` attribute, '
            'or override the `get_policy()` method.'
            % self.__class__.__name__
        )
        # pylint: disable=not-callable
        return self.policy_class(self.request, self)

    def perform_create(self, serializer):
        """ Call can_create_object with an already validated serializer

        An instance isn't available until the save has occurred
        so the `can_create_object` method is a bit unusual in
        this case by passing in the serializer only.
        """

        if hasattr(self.policy, 'can_create_object'):
            kwargs = {'validated': True}
            self.policy.can_create_object(serializer, kwargs)
        return super(PolicyViewMixin, self).perform_create(serializer)

    def perform_update(self, serializer):
        """ Call `can_update_object` with the validated instance """

        if hasattr(self.policy, 'can_update_object'):
            kwargs = {'validated': True}
            self.policy.can_update_object(serializer.instance, kwargs)
        return super(PolicyViewMixin, self).perform_update(serializer)
