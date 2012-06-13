# pylint: disable=E0211, E0213
# E0211: Method has no argument
# E0213: Method should have "self" as first argument


from zope.interface import Interface


class IQuotaAware(Interface):
    """ marker interface for objects that are quota aware.
    """


class IQuotaSupport(Interface):
    """ marker interface for containers with quota support.
    """


class IQuotaSize(Interface):
    """ an adapter that stores the size of an object used for quota
        calculation.
    """
    def get_size():
        """ return the stored size of the object.
        """

    def update_size():
        """ update and store the size of the object.
            return the difference between new and old size.
        """
