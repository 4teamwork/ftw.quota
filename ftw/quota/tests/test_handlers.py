from Products.Archetypes.interfaces import IBaseObject
from Products.CMFCore.interfaces import ISiteRoot
from ftw.quota import handlers
from ftw.quota.interfaces import IQuotaSupport
from ftw.quota.testing import ZCML_LAYER
from ftw.testing import MockTestCase


class TestFindQuotaParent(MockTestCase):

    layer = ZCML_LAYER

    def test_context_is_quota_container(self):
        context = self.providing_stub([IBaseObject, IQuotaSupport])
        self.replay()
        self.assertEqual(handlers.find_quota_parent(context), context)

    def test_parent_is_quota_container(self):
        parent = self.providing_stub([IBaseObject, IQuotaSupport])
        context = self.providing_stub([IBaseObject])
        self.set_parent(context, parent)

        self.replay()
        self.assertEqual(handlers.find_quota_parent(context), parent)

    def test_nested_quota_containers(self):
        context = self.providing_stub([IBaseObject])
        first = self.providing_stub([IBaseObject, IQuotaSupport])
        second = self.providing_stub([IBaseObject, IQuotaSupport])
        self.set_parent(context, self.set_parent(first, second))

        self.replay()
        self.assertEqual(handlers.find_quota_parent(context), first)

    def test_stop_when_site_root_reached(self):
        context = self.providing_stub([IBaseObject])
        root = self.providing_stub([IBaseObject, ISiteRoot])
        self.set_parent(context, root)

        self.replay()
        self.assertEqual(handlers.find_quota_parent(context), None)

    def test_stop_when_not_AT_object(self):
        context = self.stub()
        self.replay()
        self.assertEqual(handlers.find_quota_parent(context), None)

    def test_stop_when_parent_not_AT_object(self):
        context = self.providing_stub([IBaseObject])
        parent = self.stub()
        self.set_parent(context, parent)

        self.replay()
        self.assertEqual(handlers.find_quota_parent(context), None)

    def test_not_looping_on_wrong_input(self):
        context = None
        self.replay()
        self.assertEqual(handlers.find_quota_parent(context), None)
