# -*- coding: utf-8 -*-
import info
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setDependencies(self):
        pass

    def setTargets(self):
        self.svnTargets['master'] = 'https://github.com/nu-book/zxing-cpp.git'
        for ver in ["1.0.7", "1.0.8", "1.1.0", "1.1.1"]:
            self.targets[ver] = f"https://github.com/nu-book/zxing-cpp/archive/v{ver}.tar.gz"
            self.archiveNames[ver] = f"zxing-cpp-v{ver}.tar.gz"
            self.targetInstSrc[ver] = f"zxing-cpp-{ver}"
        self.targetDigests['1.0.7'] = (
            ['b6eacc2ca25fcf7d2ceb07900eae1f6bdef8a349c9d373df3b8481116355afbb'], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests['1.0.8'] = (
            ['9154b5456904e47bd4c38462d57e4b7897bfb20cb2bc2e8c958453e40e73c8b2'], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests['1.1.0'] = (
            ['283574a817a6efdb38e4f0480fb7697e9b1f90b55d6b16e92e1a2d2af9c43506'], CraftHash.HashAlgorithm.SHA256)
        self.patchToApply["1.1.0"] = [("zxing-cpp-1.1.0-20201112.diff", 1)]
        self.targetDigests['1.1.1'] = (
            ['e595b3fa2ec320beb0b28f6af56b1141853257c2611686685639cebb3b248c86'], CraftHash.HashAlgorithm.SHA256)
        self.defaultTarget = '1.1.1'


class Package(CMakePackageBase):
    def __init__(self, **args):
        CMakePackageBase.__init__(self)

        self.subinfo.options.configure.args += "-DBUILD_BLACKBOX_TESTS=OFF -DBUILD_EXAMPLES=OFF"
