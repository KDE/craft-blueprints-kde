import info
from Package.CMakePackageBase import CMakePackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets["master"] = "https://github.com/quotient-im/libQuotient.git||dev"

        for ver in ["0.9.0"]:
            self.targets[ver] = "https://github.com/quotient-im/libQuotient/archive/%s.tar.gz" % ver
            self.archiveNames[ver] = "libQuotient-%s.tar.gz" % ver
            self.targetInstSrc[ver] = "libQuotient-%s" % ver

        self.targetDigests["0.9.0"] = (["5e607eb978a5daa82e2186cd92f0d964cb820c72cfad95ed2adda4525ed923b5"], CraftHash.HashAlgorithm.SHA256)

        self.defaultTarget = "0.9.0"
        self.description = "A Qt library to write cross-platform clients for Matrix"

        self.patchToApply["0.9.0"] = [("fix-saving-access-token-to-keychain.diff", 1)]
        self.patchLevel["0.9.0"] = 1

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/qt/qtbase"] = None

        self.runtimeDependencies["qt-libs/qtkeychain"] = None
        self.runtimeDependencies["libs/olm"] = None


class Package(CMakePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # LINK : fatal error LNK1104: cannot open file 'Quotient.lib
        # And fixes crash on android
        self.subinfo.options.dynamic.buildStatic = True
