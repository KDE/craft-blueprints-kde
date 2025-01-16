# -*- coding: utf-8 -*-
import info
from Package.CMakePackageBase import CMakePackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def setTargets(self):
        self.description = "Freecell Solving library"
        self.webpage = "https://fc-solve.shlomifish.org/"

        # just support one version
        ver = "6.2.0"
        self.defaultTarget = ver
        self.targets[ver] = "https://fc-solve.shlomifish.org/downloads/fc-solve/freecell-solver-%s.tar.xz" % ver
        self.archiveNames[ver] = "freecell-solver-%s.tar.xz" % ver
        self.targetInstSrc[ver] = "freecell-solver-%s" % ver
        self.targetDigests[ver] = (["2267758cc00ec7e7f0c47e61f398032afb4bb5386d1e54d5164ca815547f7423"], CraftHash.HashAlgorithm.SHA256)

    def setDependencies(self):
        self.buildDependencies["libs/rinutils"] = None
        self.buildDependencies["perl-modules/path-tiny"] = None
        self.buildDependencies["perl-modules/template"] = None
        self.buildDependencies["perl-modules/module-runtime"] = None
        self.buildDependencies["perl-modules/moo"] = None
        self.buildDependencies["perl-modules/sub-quote"] = None
        self.buildDependencies["dev-utils/gperf"] = None
        self.buildDependencies["libs/python"] = None
        self.buildDependencies["dev-utils/system-python3"] = None
        self.buildDependencies["python-modules/random2"] = None
        self.buildDependencies["python-modules/six"] = None
        self.buildDependencies["python-modules/pysol-cards"] = None
        self.runtimeDependencies["virtual/base"] = None


class Package(CMakePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subinfo.options.configure.args += ["-DFCS_WITH_TEST_SUITE=OFF"]
