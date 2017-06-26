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


def _get_action(view):
    """ Return the string action name of the view """

    try:
        if view.action == 'partial_update':
            return 'update'
        return view.action
    except AttributeError:
        return 'unknown'


class PolicyPermission(permissions.BasePermission):
    """ Custom DRF permission object

    Has the expected DRF entry points for global & object
    level permissions.
    """

    def can_access(self, request, view):
        """ Always called before object fetch """

        pass

    def can_access_object(self, request, view, obj):
        """ Always called after object fetch """

        pass

    def can_write(self, request, view):
        """ Unsafe methods only before object fetch """

        pass

    def can_write_object(self, request, view, obj):
        """ Unsafe methods only after object fetch """

        pass

    def has_permission(self, request, view):
        """ DRF APIView entry point for global permissions

        A few implementation details to be aware of are the
        following:

            * can_access is always called
            * can_write is called only on unsafe methods
            * can_unknown is a fall through if no action is found
        """

        self.can_access(request, view)
        if request.method not in permissions.SAFE_METHODS:
            self.can_write(request, view)

        try:
            method_name = 'can_%s' % _get_action(view)
            getattr(self, method_name)(request, view)
        except AttributeError:
            pass

        return super().has_permission(request, view)

    def has_object_permission(self, request, view, obj):
        """ DRF APIView entry point for single object permissions

        An important point with object level perm checks in DRF
        is they're called before any data is validated. Obviously,
        before the object is mutated as well.
        """

        self.can_access_object(request, view, obj)
        if request.method not in permissions.SAFE_METHODS:
            self.can_write_object(request, view, obj)

        try:
            method_name = 'can_%s_object' % _get_action(view)
            getattr(self, method_name)(request, view, obj)
        except AttributeError:
            pass

        return super().has_object_permission(request, view, obj)
