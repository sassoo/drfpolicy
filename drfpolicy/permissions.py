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

        One thing to note is `can_read` is always called even
        if an unsafe method is being used. This is by design.
        """

        if hasattr(view.policy, 'can_read'):
            view.policy.can_read()

        if request.method not in permissions.SAFE_METHODS:
            if hasattr(view.policy, 'can_write'):
                view.policy.can_write()

        method = 'can_%s' % _get_action(view)
        if hasattr(view.policy, method):
            getattr(view.policy, method)()

        return True

    def has_object_permission(self, request, view, obj):
        """ DRF APIView entry point for single object permissions

        Just like the global perm checks the `can_read_object`
        method is called even if an unsafe method is being used.

        An important point with this object level perm checks with
        DRF is that these methods are all called before any data
        is validated. Obviously, before the object is mutated as
        well.

        The `validated` kwarg will be passed to the method with
        a value of False in this case. The `PolicyViewMixin` will
        call some of the action specific perm checks a second time
        with a validated value of True after validation is done &
        the object is mutated but still dirty. This makes perm
        checks after the modification easier.

        It pairs well with the drfchangemgmt project.
        """

        kwargs = {'validated': False}

        if hasattr(view.policy, 'can_read_object'):
            view.policy.can_read_object(obj, kwargs)

        if request.method not in permissions.SAFE_METHODS:
            if hasattr(view.policy, 'can_write_object'):
                view.policy.can_write_object(obj, kwargs)

        method = 'can_%s_object' % _get_action(view)
        if hasattr(view.policy, method):
            getattr(view.policy, method)(obj, kwargs)

        return True
