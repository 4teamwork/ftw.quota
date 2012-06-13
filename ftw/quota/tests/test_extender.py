from Products.Archetypes.interfaces import IBaseObject
from archetypes.schemaextender.field import ExtensionField
from ftw.quota.interfaces import IQuotaSupport
from ftw.quota.testing import ZCML_LAYER
from ftw.testing import MockTestCase
from zope.component import queryAdapter


class TestQuotaExtender(MockTestCase):

    layer = ZCML_LAYER

    def test_adapts_IQuotaSupport_only(self):
        obj = self.providing_stub([IBaseObject])
        self.replay()
        adapter = queryAdapter(obj, name="ftw.quota.extender.QuotaExtender")
        self.assertEqual(adapter, None)

    def test_adapts_IQuotaSupport(self):
        obj = self.providing_stub([IQuotaSupport])
        self.replay()
        adapter = queryAdapter(obj, name="ftw.quota.extender.QuotaExtender")
        self.assertNotEqual(adapter, None)

    def test_fields_are_extension_fields(self):
        obj = self.providing_stub([IQuotaSupport])
        self.replay()

        adapter = queryAdapter(obj, name="ftw.quota.extender.QuotaExtender")
        fields = adapter.getFields()

        for field in fields:
            self.assertTrue(
                isinstance(field, ExtensionField),
                msg='Field "%s" is not an ExtensionField' % field.__name__)
