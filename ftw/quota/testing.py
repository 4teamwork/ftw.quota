from ftw.testing.layer import ComponentRegistryLayer
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import setRoles, TEST_USER_ID, TEST_USER_NAME, login
from zope.configuration import xmlconfig


class ZCMLLayer(ComponentRegistryLayer):

    def setUp(self):
        super(ZCMLLayer, self).setUp()

        import ftw.quota.tests
        self.load_zcml_file('test.zcml', ftw.quota.tests)


ZCML_LAYER = ZCMLLayer()


class FtwQuotaLayer(PloneSandboxLayer):

    def setUpZope(self, app, configurationContext):
        import archetypes.schemaextender
        xmlconfig.file('configure.zcml', archetypes.schemaextender,
                       context=configurationContext)

        import ftw.quota
        xmlconfig.file('configure.zcml', ftw.quota,
                       context=configurationContext)

    def setUpPloneSite(self, portal):
        setRoles(portal, TEST_USER_ID, ['Manager'])
        login(portal, TEST_USER_NAME)


FTW_QUOTA_FIXTURE = FtwQuotaLayer()
FTW_QUOTA_INTEGRATION_TESTING = IntegrationTesting(
    bases=(FTW_QUOTA_FIXTURE, ), name="FtwQuota:Integration")
