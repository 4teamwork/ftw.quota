from borg.localrole.interfaces import IFactoryTempFolder
from ftw.quota import handlers
from ftw.quota.interfaces import IQuotaSupport, IQuotaAware
from ftw.quota.testing import ZCML_LAYER
from ftw.testing import MockTestCase
from mocker import ANY
from Products.Archetypes.interfaces import IBaseObject
from Products.CMFCore.interfaces import ISiteRoot
from zExceptions import Redirect
from zope.annotation.interfaces import IAttributeAnnotatable


class TestRaiseQuotaExceeded(MockTestCase):

    layer = ZCML_LAYER

    def test_exceeding_raised_when_quota_enforced(self):
        context = self.providing_stub(IQuotaSupport)
        self.expect(context.Schema().getField(
                'enforce').get(context)).result(True)
        self.expect(context.absolute_url()).result('/plone/foo')

        request = self.stub_request(interfaces=[IAttributeAnnotatable])
        self.expect(context.REQUEST).result(request)
        cookies = {}
        self.expect(request.cookies).result(cookies)

        plone_utils = self.mocker.mock()
        self.mock_tool(plone_utils, 'plone_utils')
        self.expect(plone_utils.addPortalMessage(ANY, 'error'))

        self.replay()

        with self.assertRaises(Redirect) as cm:
            handlers.raise_quota_exceeded(context)

        self.assertEqual(cm.exception.args, ('/plone/foo',))

    def test_no_exceeding_raised_when_not_enforced(self):
        context = self.providing_stub(IQuotaSupport)
        self.expect(context.Schema().getField(
                'enforce').get(context)).result(False)

        self.replay()
        handlers.raise_quota_exceeded(context)


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

    def test_is_in_factory(self):
        context = self.providing_stub([IFactoryTempFolder])
        first = self.stub()
        second = self.providing_stub([IBaseObject])
        third = self.providing_stub([IBaseObject, IQuotaSupport])

        self.set_parent(context,
            self.set_parent(first,
                self.set_parent(second, third)))

        self.replay()
        self.assertEqual(handlers.find_quota_parent(context), third)

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


class TestObjectAddedOrModified(MockTestCase):

    layer = ZCML_LAYER

    def test_object_added_increases_usage(self):
        container = self.providing_mock([IBaseObject, IQuotaSupport])
        context = self.providing_stub(
            [IBaseObject, IAttributeAnnotatable, IQuotaAware])
        self.set_parent(context, container)

        self.expect(context.get_size()).result(5)

        schema = self.mocker.mock()
        self.expect(container.Schema()).result(schema).count(0, None)
        self.expect(schema.getField('quota').get(container)).result(100)
        self.expect(schema.getField('usage').get(container)).result(10)
        self.expect(schema.getField('usage').set(container, 15))

        self.replay()

        handlers.object_added_or_modified(context, None)
