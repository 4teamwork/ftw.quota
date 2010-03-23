from Products.PloneTestCase import ptc
import collective.testcaselayer.ptc

ptc.setupPloneSite()

class IntegrationTestLayer(collective.testcaselayer.ptc.BasePTCLayer):

    def afterSetUp(self):          

        # import extension profile
        self.addProfile('ftw.quota:default')


layer = IntegrationTestLayer([collective.testcaselayer.ptc.ptc_layer])