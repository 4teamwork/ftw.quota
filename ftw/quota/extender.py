from archetypes.schemaextender.interfaces import ISchemaExtender
from archetypes.schemaextender.field import ExtensionField
from Products.Archetypes import atapi
from ftw.quota.interfaces import IQuotaSupport
from zope.interface import implements
from zope.component import adapts
from Products.CMFCore.permissions import ManagePortal
from ftw.quota import _


class QuotaIntegerField(ExtensionField, atapi.IntegerField):
    """An integer field for storing quotas."""


class QuotaBooleanField(ExtensionField, atapi.BooleanField):
    """A boolean field."""


class QuotaExtender(object):
    implements(ISchemaExtender)
    adapts(IQuotaSupport)
    
    fields = [
        QuotaIntegerField("quota",
            schemata = 'quota',
            required = False,
            default = 52428800,
            write_permission = ManagePortal,
            searchable = False,
                widget = atapi.IntegerWidget(
                label = _(u'label_quota', default=u'Quota (Bytes)'),
                description = _(u'help_quota', default=u''),
                size = 20,
            ),
        ),
        
        QuotaIntegerField("usage",
            schemata = 'quota',
            required = False,
            searchable = False,
            default = 0,
            write_permission = ManagePortal,
            widget = atapi.IntegerWidget(
                label = _(u'label_usage', default=u'Usage (Bytes)'),
                description = _(u'help_quota', default=u''),
                size = 20,
                #visible = {'view': 'visible', 'edit': 'invisible'},
            ),
        ),
        
        QuotaBooleanField("enforce",
            schemata = 'quota',
            required = False,
            default = True,
            write_permission = ManagePortal,
            widget = atapi.BooleanWidget(
                label = _(u'label_enforce', default=u'Enforce Quota'),
                description = _(u'help_enforce', default=u''),
            ),
        ),
    ]

    def __init__(self, context):
        self.context = context

    def getFields(self):
        return self.fields
