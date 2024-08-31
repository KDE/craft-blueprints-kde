import info
from CraftCore import CraftCore
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets["master"] = "https://github.com/quotient-im/libQuotient.git||tobias/vodozemac"

        for ver in ["0.8.1.1", "0.8.2"]:
            self.targets[ver] = "https://github.com/quotient-im/libQuotient/archive/%s.tar.gz" % ver
            self.archiveNames[ver] = "libQuotient-%s.tar.gz" % ver
            self.targetInstSrc[ver] = "libQuotient-%s" % ver

        self.targetDigests["0.8.1.1"] = (["d1ab944a4b42f68d2d2ebfb2782a3e92eac2b7e056c7f72af2ba3b3ddf2fd735"], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests["0.8.2"] = (["12ff2fa8b80a934b9dd88fa3416a4b88e94bc0e18a8df0dcebfc90614dd2f5c9"], CraftHash.HashAlgorithm.SHA256)

        self.defaultTarget = "0.8.2"
        self.description = "A Qt library to write cross-platform clients for Matrix"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/qt/qtbase"] = None

        self.runtimeDependencies["qt-libs/qtkeychain"] = None
        self.runtimeDependencies["libs/vodozemac-cpp"] = None


class Package(CMakePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # LINK : fatal error LNK1104: cannot open file 'Quotient.lib
        # And fixes crash on android
        self.subinfo.options.dynamic.buildStatic = True
        self.subinfo.options.configure.args += ["-DQuotient_ENABLE_E2EE=ON"]
        self.subinfo.options.configure.args += ["-DBUILD_WITH_QT6=ON"]
