import glob

import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.description = "StellarSolver Sextractor and Astrometry.net based Library"
        self.svnTargets["master"] = "https://github.com/rlancaste/stellarsolver.git"
        for ver in ["2.7"]:
            self.targets[ver] = "https://github.com/rlancaste/stellarsolver/archive/refs/tags/%s.tar.gz" % ver
            self.archiveNames[ver] = "stellarsolver-%s.tar.gz" % ver
            self.targetInstSrc[ver] = "stellarsolver-%s" % ver
        self.defaultTarget = "2.7"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/qt/qtbase"] = None
        self.runtimeDependencies["libs/gsl"] = None
        self.runtimeDependencies["libs/mman"] = None
        self.runtimeDependencies["libs/cfitsio"] = None
        self.runtimeDependencies["libs/zlib"] = None
        self.runtimeDependencies["boost-regex"] = None
        self.runtimeDependencies["libs/wcslib"] = None


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self):
        super().__init__()
