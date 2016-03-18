"""
    drfpolicy.permissions
    ~~~~~~~~~~~~~~~~~~~~~

    DRF policy permissions for APIView's
"""

from rest_framework import permissions


def _get_action(view):
    """ Return the string action name of the view """

    action = view.action
    if action == 'partial_update':
        action = 'update'
    return action


class PolicyPermission(permissions.BasePermission):
    """ Custom DRF permission object """

    def has_permission(self, request, view):
        """ DRF APIView entry point for global permissions """

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
        """ DRF APIView entry point for single object permissions """

        if hasattr(view.policy, 'can_read_object'):
            view.policy.can_read_object(obj)

        if request.method not in permissions.SAFE_METHODS:
            if hasattr(view.policy, 'can_write_object'):
                view.policy.can_write_object(obj)

        method = 'can_%s_object' % _get_action(view)
        if hasattr(view.policy, method):
            getattr(view.policy, method)(obj)

        return True
