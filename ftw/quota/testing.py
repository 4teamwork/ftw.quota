from ftw.testing.layer import ComponentRegistryLayer


class ZCMLLayer(ComponentRegistryLayer):

    def setUp(self):
        super(ZCMLLayer, self).setUp()

        import ftw.quota.tests
        self.load_zcml_file('test.zcml', ftw.quota.tests)


ZCML_LAYER = ZCMLLayer()
