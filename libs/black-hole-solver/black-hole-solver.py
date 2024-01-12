# -*- coding: utf-8 -*-
import info
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setTargets(self):
        self.description = "Black Hole Solitaire Solver"
        self.webpage = "https://www.shlomifish.org/open-source/projects/black-hole-solitaire-solver/"

        # just support one version
        ver = "1.10.1"
        self.defaultTarget = ver
        self.targets[ver] = "https://fc-solve.shlomifish.org/downloads/fc-solve/black-hole-solver-%s.tar.xz" % ver
        self.archiveNames[ver] = "black-hole-solver-%s.tar.xz" % ver
        self.targetInstSrc[ver] = "black-hole-solver-%s" % ver
        self.targetDigests[ver] = (["36e1953a99e02e82489a3cb109fb590bcab307b4ddaec34cb0e67347668511e2"], CraftHash.HashAlgorithm.SHA256)

    def setDependencies(self):
        self.buildDependencies["libs/rinutils"] = None
        self.buildDependencies["perl-modules/path-tiny"] = None
        self.runtimeDependencies["virtual/base"] = None


class Package(CMakePackageBase):
    def __init__(self, **args):
        super().__init__()
        self.subinfo.options.configure.args += ["-DFCS_WITH_TEST_SUITE=OFF"]
