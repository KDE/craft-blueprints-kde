# -*- coding: utf-8 -*-
import info
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/qt5/qtbase"] = None
        self.buildDependencies["libs/qt5/qttools"] = None
        self.buildDependencies["libs/libsecret"] = None

    def setTargets(self):
        self.svnTargets['master'] = 'https://github.com/frankosterfeld/qtkeychain.git'
        for ver in ["0.10.0", "0.11.0", "0.12.0"]:
            self.targets[ver] = "https://github.com/frankosterfeld/qtkeychain/archive/v%s.tar.gz" % ver
            self.archiveNames[ver] = "qtkeychain-v%s.tar.gz" % ver
            self.targetInstSrc[ver] = 'qtkeychain-%s' % ver
        self.targetDigests['0.10.0'] = (['5f916cd97843de550467db32d2e10f218b904af5b21cfdfcc7c6425d7dfc3ec2'], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests['0.12.0'] = (['cc547d58c1402f6724d3ff89e4ca83389d9e2bdcfd9ae3d695fcdffa50a625a8'], CraftHash.HashAlgorithm.SHA256)

        self.patchToApply["0.10.0"] = [("0001-Don-t-use-absolute-path-to-frameworks.patch", 1)]
        self.patchLevel["0.10.0"] = 1
        self.patchToApply["0.12.0"] = [("qtkeychain-0.12.0-20210128.diff", 1)]

        self.defaultTarget = '0.12.0'


class Package(CMakePackageBase):
    def __init__(self, **args):
        CMakePackageBase.__init__(self)
