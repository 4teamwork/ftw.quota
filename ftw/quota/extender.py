from Products.Archetypes import atapi
from Products.CMFCore.permissions import ManagePortal
from archetypes.schemaextender.field import ExtensionField
from archetypes.schemaextender.interfaces import ISchemaExtender
from ftw.quota import _
from ftw.quota.interfaces import IQuotaSupport
from zope.component import adapts
from zope.interface import implements


class QuotaIntegerField(ExtensionField, atapi.IntegerField):
    """An integer field for storing quotas."""


class QuotaBooleanField(ExtensionField, atapi.BooleanField):
    """A boolean field."""


class QuotaExtender(object):
    implements(ISchemaExtender)
    adapts(IQuotaSupport)

    fields = [

        QuotaIntegerField(
            name='quota',
            schemata='quota',
            required=False,
            default=52428800,
            write_permission=ManagePortal,
            searchable=False,
                widget=atapi.IntegerWidget(
                label=_(u'label_quota', default=u'Quota (Bytes)'),
                description=_(u'help_quota', default=u''),
                size=20)),

        QuotaIntegerField(
            name='usage',
            schemata='quota',
            required=False,
            searchable=False,
            default=0,
            write_permission=ManagePortal,
            widget=atapi.IntegerWidget(
                label=_(u'label_usage', default=u'Usage (Bytes)'),
                description=_(u'help_quota', default=u''),
                size=20)),

        QuotaBooleanField(
            name='enforce',
            schemata='quota',
            required=False,
            default=True,
            write_permission=ManagePortal,
            widget=atapi.BooleanWidget(
                label=_(u'label_enforce', default=u'Enforce Quota'),
                description=_(u'help_enforce', default=u''))),

    ]

    def __init__(self, context):
        self.context = context

    def getFields(self):
        """Returns this schema's fields
        """
        return self.fields
