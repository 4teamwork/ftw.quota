from zope.interface import implements
from zope.annotation.interfaces import IAnnotations
from zope.component import adapts
from ftw.quota.interfaces import IQuotaSize
from Products.Archetypes.interfaces import IBaseObject

QUOTAKEY = 'ftw.quota.size'


class QuotaSizeAnnotation(object):
    """ an adapter that stores the size of an object used for quota
        calculation in an annotation.
    """
    implements(IQuotaSize)
    adapts(IBaseObject)

    def __init__(self, context):
        self.context = context

    def update_size(self):
        ann = IAnnotations(self.context)
        old_size = ann.get(QUOTAKEY, 0)
        new_size = self.context.get_size()
        ann[QUOTAKEY] = new_size
        return new_size - old_size

    def get_size(self):
        ann = IAnnotations(self.context)
        size = ann.get(QUOTAKEY, None)
        if size is not None:
            return size
        return self.update_size()
