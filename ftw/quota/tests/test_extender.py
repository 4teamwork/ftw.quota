from archetypes.schemaextender.field import ExtensionField
from ftw.builder import Builder
from ftw.builder import create
from ftw.quota.testing import FTW_QUOTA_INTEGRATION_TESTING
from unittest2 import TestCase
from zope.component import queryAdapter


class TestQuotaExtender(TestCase):
    layer = FTW_QUOTA_INTEGRATION_TESTING

    def test_adapts_IQuotaSupport_only(self):
        context = create(Builder('file'))
        adapter = queryAdapter(context, name="ftw.quota.extender.QuotaExtender")
        self.assertFalse(adapter)

    def test_adapts_IQuotaSupport(self):
        context = create(Builder('folder'))
        adapter = queryAdapter(context, name="ftw.quota.extender.QuotaExtender")
        self.assertTrue(adapter)

    def test_fields_are_extension_fields(self):
        context = create(Builder('folder'))
        adapter = queryAdapter(context, name="ftw.quota.extender.QuotaExtender")
        fields = adapter.getFields()

        for field in fields:
            self.assertTrue(
                isinstance(field, ExtensionField),
                msg='Field "%s" is not an ExtensionField' % field.__name__)
