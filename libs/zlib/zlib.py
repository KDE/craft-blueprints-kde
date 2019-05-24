# -*- coding: utf-8 -*-
import info
from Package.AutoToolsPackageBase import AutoToolsPackageBase
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ['1.2.11']:
            self.targets[ver] = 'http://downloads.sourceforge.net/sourceforge/libpng/zlib-%s.tar.gz' % ver
            self.targetInstSrc[ver] = "zlib-" + ver

        if CraftCore.compiler.isWindows:
            self.patchToApply['1.2.11'] = [("zlib-1.2.11-20180203.diff", 1),
                                           ("zlib-1.2.11-20190509.diff", 1)  # its a cmake define, don't change it
                                           ]
        self.patchLevel["1.2.11"] = 2
        self.targetDigests['1.2.11'] = (['c3e5e9fdd5004dcb542feda5ee4f0ff0744628baf8ed2dd5d66f8ca1197cb1a1'], CraftHash.HashAlgorithm.SHA256)

        self.description = 'The zlib compression and decompression library'
        self.defaultTarget = '1.2.11'

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None


if CraftCore.compiler.isWindows:
    class Package(CMakePackageBase):
        def __init__(self, **args):
            CMakePackageBase.__init__(self)
else:
    class Package(AutoToolsPackageBase):
        def __init__(self, **args):
            AutoToolsPackageBase.__init__(self)
            self.subinfo.options.configure.autoreconf = False
            self.platform = ""