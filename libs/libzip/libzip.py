# -*- coding: utf-8 -*-
import info


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ['0.9', '0.9.3']:
            self.targets[ver] = "https://libzip.org/download/libzip-" + ver + ".tar.bz2"
            self.targetInstSrc[ver] = "libzip-" + ver
        for ver in ['0.11.1', '1.5.1']:
            self.targets[ver] = "https://libzip.org/download/libzip-" + ver + ".tar.xz"
            self.targetInstSrc[ver] = "libzip-" + ver
        self.patchToApply['0.9.0'] = ('libzip-0.9.diff', 1)
        self.patchToApply['0.9.3'] = ('libzip-0.9.3-20101116.diff', 1)
        self.patchToApply['0.11.1'] = ('libzip-0.11.1-20130907.diff', 1)
        self.patchToApply['1.5.1'] = ('libzip-1.5.1-20180423.diff', 1)
        self.targetDigests['0.9.3'] = '16e94bc0327f1a76a0296a28908cf6439b0a0a67'
        self.targetDigests['0.11.1'] = '3c82cdc0de51f06d5e1c60f098d3d9cc0d48f8a7'
        self.targetDigests['1.5.1'] = (['04ea35b6956c7b3453f1ed3f3fe40e3ddae1f43931089124579e8384e79ed372'], CraftHash.HashAlgorithm.SHA256)

        self.description = "a library for handling zip archives"
        self.defaultTarget = '1.5.1'

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/zlib"] = None
        self.runtimeDependencies["libs/nettle"] = None
        self.runtimeDependencies["libs/gnutls"] = None


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
