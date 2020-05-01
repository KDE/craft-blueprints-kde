# -*- coding: utf-8 -*-
import info


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["4.2.0", "4.3.0"]:
            self.targets[ver] = 'https://github.com/opencv/opencv_contrib/archive/' + ver + '.tar.gz'
            self.targetInstSrc[ver] = 'opencv_contrib-' + ver

        self.targetDigests['4.2.0'] = (['8a6b5661611d89baa59a26eb7ccf4abb3e55d73f99bb52d8f7c32265c8a43020'], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests['4.3.0'] = (['acb8e89c9e7d1174e63e40532125b60d248b00e517255a98a419d415228c6a55'], CraftHash.HashAlgorithm.SHA256)
        self.defaultTarget = '4.3.0'

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/opencv"] = None


from Package.VirtualPackageBase import *


class Package(SourceComponentPackageBase):
    def __init__(self, **args):
        SourceComponentPackageBase.__init__(self)
