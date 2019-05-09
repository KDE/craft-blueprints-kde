# -*- coding: utf-8 -*-
import info
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ['1.2.5', '1.2.6', '1.2.7', '1.2.8', '1.2.11']:
            self.targets[ver] = 'http://downloads.sourceforge.net/sourceforge/libpng/zlib-%s.tar.gz' % ver
            self.targetInstSrc[ver] = "zlib-" + ver
        self.patchToApply['1.2.5'] = [("zlib-1.2.5-20110629.diff", 1)]
        self.patchToApply['1.2.6'] = [("zlib-1.2.6-20120421.diff", 1)]
        self.patchToApply['1.2.7'] = [("zlib-1.2.7-20130123.diff", 1)]
        self.patchToApply['1.2.8'] = [("zlib-1.2.8-20130901.diff", 1)]
        self.patchToApply['1.2.11'] = [("zlib-1.2.11-20180203.diff", 1),
                                       ("zlib-1.2.11-20190509.diff", 1)  # its a cmake define, don't change it
                                       ]
        self.patchLevel["1.2.11"] = 2
        self.targetDigests['1.2.5'] = '8e8b93fa5eb80df1afe5422309dca42964562d7e'
        self.targetDigests['1.2.7'] = '4aa358a95d1e5774603e6fa149c926a80df43559'
        self.targetDigests['1.2.8'] = 'a4d316c404ff54ca545ea71a27af7dbc29817088'
        self.targetDigests['1.2.11'] = (['c3e5e9fdd5004dcb542feda5ee4f0ff0744628baf8ed2dd5d66f8ca1197cb1a1'], CraftHash.HashAlgorithm.SHA256)

        self.description = 'The zlib compression and decompression library'
        self.defaultTarget = '1.2.11'

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None


class Package(CMakePackageBase):
    def __init__(self, **args):
        CMakePackageBase.__init__(self)
