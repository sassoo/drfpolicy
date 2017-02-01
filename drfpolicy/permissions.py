"""
    drfpolicy.permissions
    ~~~~~~~~~~~~~~~~~~~~~

    DRF policy permissions for APIView's

    This makes permission handling more DRY & moves the
    permissions to a centralized single-source-of-truth.
    Namely, a policy object.

    The policy object can opt-in to any of the permission
    checks by logical names. The logic on what is called &
    when is very easily seen in the code below.
"""

from rest_framework import permissions


__all__ = ('PolicyPermission',)


def _get_action(view):
    """ Return the string action name of the view """

    action = view.action
    if action == 'partial_update':
        action = 'update'
    return action


class PolicyPermission(permissions.BasePermission):
    """ Custom DRF permission object

    Has the expected DRF entry points for global & object
    level permissions.
    """

    def has_permission(self, request, view):
        """ DRF APIView entry point for global permissions

        A few implementation details to be aware of are the
        following:

            * can_access is always called
            * can_read is called only on safe methods
            * can_write is called only on unsafe methods
        """

        if hasattr(view.policy, 'can_access'):
            view.policy.can_access()

        if request.method in permissions.SAFE_METHODS:
            if hasattr(view.policy, 'can_read'):
                view.policy.can_read()
        elif hasattr(view.policy, 'can_write'):
            view.policy.can_write()

        method = 'can_%s' % _get_action(view)
        if hasattr(view.policy, method):
            getattr(view.policy, method)()

        return True

    def has_object_permission(self, request, view, obj):
        """ DRF APIView entry point for single object permissions

        An important point with object level perm checks in DRF
        is that called before any data is validated. Obviously,
        before the object is mutated as well & so to are any
        subsequent policy methods.

        The `validated` kwarg will be passed to the method with
        a value of False in this case. The `PolicyViewMixin` will
        call some of the action specific perm checks a second time
        with a validated value of True after validation is done &
        the object is mutated but still dirty. This makes perm
        checks after the modification easier.

        It pairs well with the drfchangemgmt project.
        """

        if hasattr(view.policy, 'can_read_object'):
            view.policy.can_read_object(obj, validated=False)

        if request.method not in permissions.SAFE_METHODS:
            if hasattr(view.policy, 'can_write_object'):
                view.policy.can_write_object(obj, validated=False)

        method = 'can_%s_object' % _get_action(view)
        if hasattr(view.policy, method):
            getattr(view.policy, method)(obj, validated=False)

        return True
