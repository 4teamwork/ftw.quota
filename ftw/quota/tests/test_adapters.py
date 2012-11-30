from Products.Archetypes.interfaces import IBaseObject
from ftw.quota.interfaces import IQuotaSize
from ftw.quota.testing import ZCML_LAYER
from ftw.testing import MockTestCase
from zope.annotation.interfaces import IAttributeAnnotatable
from zope.component import queryAdapter


class TestQuotaSizeAnnotation(MockTestCase):

    layer = ZCML_LAYER

    def setUp(self):
        super(TestQuotaSizeAnnotation, self).setUp()
        self.context = self.providing_stub(
            [IBaseObject, IAttributeAnnotatable])

    def test_component_registered(self):
        self.replay()

        self.assertNotEquals(queryAdapter(self.context, IQuotaSize), None)

    def test_size_is_stored(self):
        self.expect(self.context.get_size()).result(10)
        self.replay()

        size = queryAdapter(self.context, IQuotaSize)
        size.update_size()
        self.assertEqual(size.get_size(), 10)

    def test_updating_size_returns_difference(self):
        with self.mocker.order():
            self.expect(self.context.get_size()).result(30)
            self.expect(self.context.get_size()).result(50)
            self.expect(self.context.get_size()).result(40)

        self.replay()

        size = queryAdapter(self.context, IQuotaSize)

        self.assertEqual(size.update_size(), 30)
        self.assertEqual(size.get_size(), 30)

        self.assertEqual(size.update_size(), 20)
        self.assertEqual(size.get_size(), 50)

        self.assertEqual(size.update_size(), -10)
        self.assertEqual(size.get_size(), 40)

    def test_get_size_updates_size(self):
        self.expect(self.context.get_size()).result(20)

        self.replay()
        size = queryAdapter(self.context, IQuotaSize)
        self.assertEqual(size.get_size(), 20)
        self.assertEqual(size.get_size(), 20)
