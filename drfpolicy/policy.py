"""
    drfpolicy.policy
    ~~~~~~~~~~~~~~~~

    Base policy object to be used when constructing policies
    for app objects.

    The BasePolicy should be inherited & have its authorization
    methods overridden when needed. See how they are called
    in the PolicyPermission object.
"""


__all__ = ('BasePolicy',)


class BasePolicy(object):
    """ Generic base policy object

    All methods that are called by the PolicyPermission object
    are explicitely shown below for clarity but they are all
    futile unless overridden.

    Return codes are ignored & you should instead raise an
    excpetion upon authorization failure.
    """

    def __init__(self, request, view):

        self.request = request
        self.view = view
