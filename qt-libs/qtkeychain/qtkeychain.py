# -*- coding: utf-8 -*-
import info
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/qt5/qtbase"] = None
        self.buildDependencies["libs/qt5/qttools"] = None

    def setTargets(self):
        self.svnTargets['master'] = 'https://github.com/frankosterfeld/qtkeychain.git'
        for ver in ["0.4.0", "0.5.0", "0.7.0", "0.8.0", "0.9.0", "0.9.1", "0.10.0"]:
            self.targets[ver] = "https://github.com/frankosterfeld/qtkeychain/archive/v%s.tar.gz" % ver
            self.archiveNames[ver] = "qtkeychain-v%s.tar.gz" % ver
            self.targetInstSrc[ver] = 'qtkeychain-%s' % ver
        self.targetDigests['0.4.0'] = '869ed20d15cc78ab3903701faf3100d639c3da57'
        self.targetDigests['0.5.0'] = (
            ['e62d7ae9c8ae04784d8a5d0f213aaa22f1c02427e800ce88739e997f499bb514'], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests['0.7.0'] = (
            ['9f9afaae8e909391d7fc932bac95e38befaac5b2eb49f6623a8efec60a2e6a3a'], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests['0.8.0'] = (
            ['b492f603197538bc04b2714105b1ab2b327a9a98d400d53d9a7cb70edd2db12f'], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests['0.9.0'] = (
            ['0935e5eb67fbed0b2db5e74ea8cbd667c6be6eed3767f212eac6ac318ab8a6fc'], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests['0.9.1'] = (
            ['9c2762d9d0759a65cdb80106d547db83c6e9fdea66f1973c6e9014f867c6f28e'], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests['0.10.0'] = (['5f916cd97843de550467db32d2e10f218b904af5b21cfdfcc7c6425d7dfc3ec2'], CraftHash.HashAlgorithm.SHA256)
        self.defaultTarget = '0.10.0'


class Package(CMakePackageBase):
    def __init__(self, **args):
        CMakePackageBase.__init__(self)
