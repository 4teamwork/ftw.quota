from ftw.quota.interfaces import IQuotaSupport
from Products.CMFCore.interfaces import ISiteRoot
from Acquisition import aq_parent
from zExceptions import Redirect
from Products.CMFCore.utils import getToolByName
from Products.Archetypes.interfaces import IBaseObject
from Products.statusmessages import STATUSMESSAGEKEY
from zope.annotation.interfaces import IAnnotations
from ftw.quota.interfaces import IQuotaSize
from ftw.quota import _


def raise_quota_exceeded(parent):
    """ add a status message and abort the current transaction by raising an
        exception.
    """
    # do nothing if quota enforcment is disabled
    schema = parent.Schema()
    if not schema.getField('enforce').get(parent):
        return

    # remove any status messages that have been added so far.
    # we will abort the current transaction, thus they are propably not
    # appropriate.
    request = parent.REQUEST
    annotations = IAnnotations(request)
    request.cookies[STATUSMESSAGEKEY] = None
    annotations[STATUSMESSAGEKEY] = None

    # add our own status message
    putils = getToolByName(parent, 'plone_utils')
    putils.addPortalMessage(_(u'msg_quota_exceeded',
                              default=u'Quota exceeded.'), 'error')
    raise Redirect, parent.absolute_url()

def find_quota_parent(parent):
    """ find a parent container that has quota support.
    """
    if not IBaseObject.providedBy(parent):
        return None
    while not IQuotaSupport.providedBy(parent) and not ISiteRoot.providedBy(parent):
        parent = aq_parent(parent)
    if IQuotaSupport.providedBy(parent):
        return parent
    return None

def object_added_or_modified(obj, event):
    """ handle adding and modifying of objects.
    """
    dsize = IQuotaSize(obj).update_size()
    if dsize == 0:
        return

    parent = aq_parent(obj)
    parent = find_quota_parent(parent)
    if parent is not None:
        # get current quota
        schema = parent.Schema()
        quota = schema.getField('quota').get(parent)
        used = schema.getField('usage').get(parent)
        if used + dsize > quota:
            raise_quota_exceeded(parent)
        # update usage
        schema.getField('usage').set(parent, used+dsize)


def object_moved(obj, event):
    """ handle copy/cut/paste of objects.
    """
    # don't deal with unfinished archetypes objects
    if obj.checkCreationFlag():
        return

    size = IQuotaSize(obj).get_size()
    if size == 0:
        return

    if event.oldParent is not None:
        parent = find_quota_parent(event.oldParent)
        if parent is not None:
            schema = parent.Schema()
            used = schema.getField('usage').get(parent)
            schema.getField('usage').set(parent, used-size)

    if event.newParent is not None:
        parent = find_quota_parent(event.newParent)
        if parent is not None:
            schema = parent.Schema()
            quota = schema.getField('quota').get(parent)
            used = schema.getField('usage').get(parent)
            if used + size > quota:
                raise_quota_exceeded(parent)
            schema.getField('usage').set(parent, used+size)
