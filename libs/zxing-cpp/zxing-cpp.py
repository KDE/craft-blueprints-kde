# -*- coding: utf-8 -*-
import info
from Package.CMakePackageBase import *

class subinfo(info.infoclass):
    def setDependencies(self):
        pass

    def setTargets(self):
        self.svnTargets['master'] = 'https://github.com/zxing-cpp/zxing-cpp.git'
        self.defaultTarget = '2.0.0'
        self.targets[self.defaultTarget] = f"https://github.com/zxing-cpp/zxing-cpp/archive/v{self.defaultTarget}.tar.gz"
        self.archiveNames[self.defaultTarget] = f"zxing-cpp-v{self.defaultTarget}.tar.gz"
        self.targetInstSrc[self.defaultTarget] = f"zxing-cpp-{self.defaultTarget}"
        self.targetDigests[self.defaultTarget] = (
            ['12b76b7005c30d34265fc20356d340da179b0b4d43d2c1b35bcca86776069f76'], CraftHash.HashAlgorithm.SHA256)
        self.patchToApply['2.0.0'] = [('0001-missing-stdexcept-include.patch', 1)]
        self.patchLevel['2.0.0'] = 1


class Package(CMakePackageBase):
    def __init__(self, **args):
        CMakePackageBase.__init__(self)

        self.subinfo.options.configure.args += "-DBUILD_DEPENDENCIES=LOCAL -DBUILD_EXAMPLES=OFF -DBUILD_UNIT_TESTS=OFF -DBUILD_BLACKBOX_TESTS=OFF"
