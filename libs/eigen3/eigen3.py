# -*- coding: utf-8 -*-
import info
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setTargets(self):
        self.description = "C++ template library for linear algebra"
        self.webpage = "http://eigen.tuxfamily.org/"

        # just support one version
        ver = "3.3.7"
        self.defaultTarget = ver
        self.targets[ver] = "http://bitbucket.org/eigen/eigen/get/%s.tar.bz2" % ver
        self.archiveNames[ver] = "eigen-%s.tar.bz2" % ver
        self.targetInstSrc[ver] = "eigen-eigen-323c052e1731"
        self.targetDigests[ver] =  (['9f13cf90dedbe3e52a19f43000d71fdf72e986beb9a5436dddcd61ff9d77a3ce'], CraftHash.HashAlgorithm.SHA256)

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None


class Package(CMakePackageBase):
    def __init__(self, **args):
        CMakePackageBase.__init__(self)
        self.subinfo.options.configure.args += " -DEIGEN_TEST_NOQT=ON -DBUILD_TESTING=ON"
