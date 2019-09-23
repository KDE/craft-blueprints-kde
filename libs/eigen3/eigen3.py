# -*- coding: utf-8 -*-
import info
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setTargets(self):
        self.description = "C++ template library for linear algebra"
        self.webpage = "http://eigen.tuxfamily.org/"

        # just support one version
        ver = "3.3.4"
        self.defaultTarget = ver
        self.targets[ver] = "http://bitbucket.org/eigen/eigen/get/%s.tar.bz2" % ver
        self.archiveNames[ver] = "eigen-%s.tar.bz2" % ver
        self.targetInstSrc[ver] = "eigen-eigen-5a0156e40feb"
        self.targetDigests[ver] =  (['dd254beb0bafc695d0f62ae1a222ff85b52dbaa3a16f76e781dce22d0d20a4a6'], CraftHash.HashAlgorithm.SHA256)

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None


class Package(CMakePackageBase):
    def __init__(self, **args):
        CMakePackageBase.__init__(self)
        self.subinfo.options.configure.args += " -DEIGEN_TEST_NOQT=ON -DBUILD_TESTING=ON"
