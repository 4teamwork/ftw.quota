from ftw.builder import Builder
from ftw.builder import create
from ftw.quota.interfaces import IQuotaSize
from ftw.quota.testing import FTW_QUOTA_INTEGRATION_TESTING
from StringIO import StringIO
from unittest2 import TestCase
from zope.component import queryAdapter


def make_file_like_object(content, filename='foo.doc'):
    data = StringIO(content)
    data.filename = filename
    return data


class TestQuotaSizeAnnotation(TestCase):
    layer = FTW_QUOTA_INTEGRATION_TESTING

    def test_size_is_stored(self):
        doc = create(Builder('file').attach_file_containing(' ' * 30))
        size = queryAdapter(doc, IQuotaSize)
        self.assertEqual(30, size.get_size())

    def test_updating_size_returns_difference(self):
        doc = create(Builder('file').attach_file_containing(''))
        size = queryAdapter(doc, IQuotaSize)
        self.assertEqual(0, size.get_size())

        doc.setFile(make_file_like_object(' ' * 10))
        self.assertEqual(10, size.update_size())
        self.assertEqual(10, size.get_size())

        doc.setFile(make_file_like_object(' ' * 30))
        self.assertEqual(20, size.update_size())
        self.assertEqual(30, size.get_size())

    def test_get_size_updates_size_only_on_first_call(self):
        doc = create(Builder('file').attach_file_containing(' ' * 10))
        size = queryAdapter(doc, IQuotaSize)

        self.assertEqual(10, size.get_size())
        doc.setFile(make_file_like_object(' ' * 20))
        self.assertEqual(10, size.get_size())
