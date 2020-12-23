# -*- coding: utf-8 -*-
import info
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None

    def setTargets(self):
        self.svnTargets['master'] = 'https://github.com/TheOneRing/vsd.git'
        self.defaultTarget = 'master'


class Package(CMakePackageBase):
    def __init__(self, **args):
        CMakePackageBase.__init__(self)
        self.subinfo.options.configure.args += ["-DSTATIC_VSD=ON"]

    def createPackage(self):
        self.ignoredPackages.append("libs/runtime")
        return super().createPackage()
