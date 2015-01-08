from ftw.builder import Builder
from ftw.builder import create
from ftw.quota import handlers
from ftw.quota.testing import FTW_QUOTA_INTEGRATION_TESTING
from unittest2 import TestCase
from zExceptions import Redirect


class TestRaiseQuotaExceeded(TestCase):
    layer = FTW_QUOTA_INTEGRATION_TESTING

    def test_exceeding_raised_when_quota_enforced(self):
        context = create(Builder('folder')
                         .having(enforce=True))
        with self.assertRaises(Redirect) as cm:
            handlers.raise_quota_exceeded(context)
        self.assertEqual(cm.exception.args, ('http://nohost/plone/folder',))

    def test_no_exceeding_raised_when_not_enforced(self):
        context = create(Builder('folder')
                         .having(enforce=False))
        handlers.raise_quota_exceeded(context)

    def test_context_is_quota_container(self):
        folder = create(Builder('folder'))
        self.assertEqual(folder, handlers.find_quota_parent(folder))

    def test_parent_is_quota_container(self):
        folder = create(Builder('folder'))
        document = create(Builder('file').within(folder))
        self.assertEqual(folder, handlers.find_quota_parent(document))

    def test_stop_when_site_root_reached(self):
        document = create(Builder('file'))
        self.assertEqual(None, handlers.find_quota_parent(document))


class TestObjectAddedOrModified(TestCase):
    layer = FTW_QUOTA_INTEGRATION_TESTING

    def test_object_added_increases_usage(self):
        folder = create(Builder('folder'))
        self.assertEquals(0, folder.getField('usage').get(folder))
        create(Builder('file')
               .within(folder)
               .attach_file_containing(' ' * 10))
        self.assertEquals(10, folder.getField('usage').get(folder))
