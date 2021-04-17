# -*- coding: utf-8 -*-
import info
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setTargets(self):
        self.description = "Freecell Solving library"
        self.webpage = "https://fc-solve.shlomifish.org/"

        # just support one version
        ver = "5.14.0"
        self.defaultTarget = ver
        self.targets[ver] = "https://fc-solve.shlomifish.org/downloads/fc-solve/freecell-solver-%s.tar.xz" % ver
        self.archiveNames[ver] = "freecell-solver-%s.tar.xz" % ver
        self.targetInstSrc[ver] = "freecell-solver-%s" % ver
        self.targetDigests[ver] =  (['b09e7394181fcd972436fbbcd2192a9085b8924b70c892ad88b9ad95a7abee12'], CraftHash.HashAlgorithm.SHA256)

    def setDependencies(self):
        self.buildDependencies["perl-modules/path-tiny"] = None
        self.buildDependencies["perl-modules/template"] = None
        self.buildDependencies["dev-utils/gperf"] = None
        self.buildDependencies["dev-utils/python3"] = None
        self.buildDependencies["python-modules/random2"] = None
        self.buildDependencies["python-modules/six"] = None
        self.buildDependencies["python-modules/pysol-cards"] = None
        self.runtimeDependencies["virtual/base"] = None


class Package(CMakePackageBase):
    def __init__(self, **args):
        CMakePackageBase.__init__(self)
        self.subinfo.options.configure.args += " -DFCS_WITH_TEST_SUITE=OFF"
