"""
    drfpolicy.permissions
    ~~~~~~~~~~~~~~~~~~~~~

    DRF policy permissions for APIView's

    This makes permission handling more DRY & logical by
    having logically named methods on a standard DRF
    permission object for more robust permission checking.

    Including pre & post serializer validation permission
    methods.
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

        try:
            self.can_access(request, view)
        except AttributeError:
            pass

        try:
            if request.method in permissions.SAFE_METHODS:
                self.can_read(request, view)
            else:
                self.can_write(request, view)
        except AttributeError:
            pass

        method = 'can_%s' % _get_action(view)
        try:
            getattr(self, method)(request, view)
        except AttributeError:
            pass

        return super().has_permission(request, view)

    def has_object_permission(self, request, view, obj):
        """ DRF APIView entry point for single object permissions

        An important point with object level perm checks in DRF
        is they're called before any data is validated. Obviously,
        before the object is mutated as well.
        """

        try:
            self.can_read_object(request, view, obj)
        except AttributeError:
            pass

        try:
            if request.method not in permissions.SAFE_METHODS:
                self.can_write_object(request, view, obj)
        except AttributeError:
            pass

        method = 'can_%s_object' % _get_action(view)
        try:
            getattr(self, method)(request, view, obj)
        except AttributeError:
            pass

        return super().has_object_permission(request, view, obj)
