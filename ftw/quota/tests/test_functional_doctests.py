import unittest
import doctest

from Testing import ZopeTestCase
from Products.PloneTestCase import ptc
from ftw.quota.tests import layer

MODULENAMES = [
]

TESTFILES = [
    'tests/quota.txt',
]

OPTIONFLAGS = (doctest.NORMALIZE_WHITESPACE|
               doctest.ELLIPSIS|
               doctest.REPORT_NDIFF)


def test_suite():

    suite = unittest.TestSuite()

    for testfile in TESTFILES:
        suite.addTest(ZopeTestCase.FunctionalDocFileSuite(
            testfile,
            optionflags=OPTIONFLAGS,
            test_class=ptc.FunctionalTestCase,
            package="ftw.quota", ))

    for module in MODULENAMES:
        suite.addTest(ZopeTestCase.FunctionalDocTestSuite(
            module,
            optionflags=OPTIONFLAGS,
            test_class=ptc.FunctionalTestCase, ))

    suite.layer = layer.layer

    return suite

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
