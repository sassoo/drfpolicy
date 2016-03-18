"""
    drfpolicy.policy
    ~~~~~~~~~~~~~~~~

    Base policy object to be used when constructing policies
    for app objects.
"""

from django.db.models.query import QuerySet


__all__ = ('BasePolicy',)


class BasePolicy(object):
    """ Generic base policy object """

    def __init__(self, request, view):

        self.request = request
        self.user = getattr(request, 'user', None)
        self.view = view

    # General
    def can_read(self):
        """ Global read access """

        return True

    # pylint: disable=unused-argument
    def can_read_object(self, obj):
        """ Read access on an individual object

        This will be called even if writes are being
        performed on the object since it first must be
        read.
        """

        return True

    def can_write(self):
        """ Global write access """

        return True

    def can_write_object(self, obj):
        """ Write access on an individual object

        This covers updates & deletes for a single object.
        In the case of updates, this is called before the
        object has been modified & before the updated data
        has been validated.
        """

        return True

    # Actions
    def can_create(self):
        """ Global create access (POST method) """

        return True

    def can_create_object(self, serializer):
        """ Create access on an individual object

        An instance isn't available until a save has occurred
        so this method is a bit unusual because it is given
        a serializer without an instance. The serializer has
        already been validated though.
        """

        return True

    def can_destroy(self):
        """ Global destroy access (DELETE method) """

        return True

    def can_destroy_object(self, obj):
        """ Destroy access on an individual object """

        return True

    def can_list(self):
        """ Global list access for a collection of resources """

        return True

    def can_retrieve(self):
        """ Global retrieve access (GET method) """

        return True

    def can_retrieve_object(self, obj):
        """ Retrieve access on an individual object

        This is NOT called when fetching a single resource
        prior to some sort of write like the `can_read_object`
        method is.
        """

        return True

    def can_update(self):
        """ Global update access (PATCH & PUT methods) """

        return True

    def can_update_object(self, obj, valid=False):
        """ Update access on an individual object

        If `valid=False` then the object has not yet been
        modified & the updated data has not been validated.

        If `valid=True` then the object has been modified &
        the updated data has been validated.

        NOTE: this method is called twice
        """

        return True

    def filter_queryset(self):
        """ Return an array of mandatory filters

        In most cases this can be an array of django `Q`
        objects that may vary depending on the requestor.

        It will be called by the drfpolicy `PolicyFilter`
        if used in views & applied to the views queryset.
        """

        return []

    def get_queryset(self):
        """ deprecate ?? what about related querysets? """

        queryset = getattr(self, 'queryset', None)
        if isinstance(queryset, QuerySet):
            # queryset is re-evaluated on each request
            queryset = queryset.all()
        return queryset

    def get_serializer_class(self):
        """ Return the serializer class """

        return getattr(self, 'serializer_class', None)
