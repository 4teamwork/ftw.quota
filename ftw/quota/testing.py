from ftw.builder.testing import BUILDER_LAYER
from ftw.quota.interfaces import IQuotaSupport
from ftw.testing.layer import ComponentRegistryLayer
from plone.app.testing import IntegrationTesting
from plone.app.testing import login
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from Products.ATContentTypes.content.folder import ATFolder
from zope.configuration import xmlconfig
from zope.interface import classImplements


class ZCMLLayer(ComponentRegistryLayer):

    def setUp(self):
        super(ZCMLLayer, self).setUp()

        import ftw.quota.tests
        self.load_zcml_file('test.zcml', ftw.quota.tests)


ZCML_LAYER = ZCMLLayer()


class FtwQuotaLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE, BUILDER_LAYER)

    def setUpZope(self, app, configurationContext):
        import archetypes.schemaextender
        xmlconfig.file('configure.zcml', archetypes.schemaextender,
                       context=configurationContext)

        import ftw.quota
        xmlconfig.file('configure.zcml', ftw.quota,
                       context=configurationContext)

        # let folders always have quotas enabled in tests.
        classImplements(ATFolder, IQuotaSupport)

    def setUpPloneSite(self, portal):
        setRoles(portal, TEST_USER_ID, ['Manager'])
        login(portal, TEST_USER_NAME)


FTW_QUOTA_FIXTURE = FtwQuotaLayer()
FTW_QUOTA_INTEGRATION_TESTING = IntegrationTesting(
    bases=(FTW_QUOTA_FIXTURE, ), name="FtwQuota:Integration")
