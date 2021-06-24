# -*- coding: utf-8 -*-
import info
from Package.CMakePackageBase import *

class subinfo(info.infoclass):
    def setDependencies(self):
        pass

    def setTargets(self):
        self.svnTargets['master'] = 'https://github.com/nu-book/zxing-cpp.git'
        self.defaultTarget = '1.2.0'
        self.targets[self.defaultTarget] = f"https://github.com/nu-book/zxing-cpp/archive/v{self.defaultTarget}.tar.gz"
        self.archiveNames[self.defaultTarget] = f"zxing-cpp-v{self.defaultTarget}.tar.gz"
        self.targetInstSrc[self.defaultTarget] = f"zxing-cpp-{self.defaultTarget}"
        self.targetDigests[self.defaultTarget] = (
            ['653d9e44195d86cf64a36af9ff3a1978ec5599df3882439fefa56e7064f55e8a'], CraftHash.HashAlgorithm.SHA256)

class Package(CMakePackageBase):
    def __init__(self, **args):
        CMakePackageBase.__init__(self)

        self.subinfo.options.configure.args += "-DBUILD_BLACKBOX_TESTS=OFF -DBUILD_EXAMPLES=OFF"
