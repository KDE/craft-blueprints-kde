# -*- coding: utf-8 -*-
import info
from Package.CMakePackageBase import *

class subinfo(info.infoclass):
    def setDependencies(self):
        pass

    def setTargets(self):
        self.svnTargets['master'] = 'https://github.com/nu-book/zxing-cpp.git'
        self.defaultTarget = '1.3.0'
        self.targets[self.defaultTarget] = f"https://github.com/nu-book/zxing-cpp/archive/v{self.defaultTarget}.tar.gz"
        self.archiveNames[self.defaultTarget] = f"zxing-cpp-v{self.defaultTarget}.tar.gz"
        self.targetInstSrc[self.defaultTarget] = f"zxing-cpp-{self.defaultTarget}"
        self.targetDigests[self.defaultTarget] = (
            ['bfd8fc706def30e34f96088b5a7afdbe0917831e57a774d34e3ee864b01c6891'], CraftHash.HashAlgorithm.SHA256)

class Package(CMakePackageBase):
    def __init__(self, **args):
        CMakePackageBase.__init__(self)

        self.subinfo.options.configure.args += "-DBUILD_DEPENDENCIES=LOCAL -DBUILD_EXAMPLES=OFF -DBUILD_UNIT_TESTS=OFF -DBUILD_BLACKBOX_TESTS=OFF"
