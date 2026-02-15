import info
from Package.CMakePackageBase import CMakePackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def registerOptions(self):
        # LINK : fatal error LNK1104: cannot open file 'Quotient.lib
        # And fixes crash on android
        self.options.dynamic.setDefault("buildStatic", True)

    def setTargets(self):
        self.svnTargets["master"] = "https://github.com/quotient-im/libQuotient.git||dev"
        self.svnTargets["rust"] = "https://github.com/quotient-im/libQuotient.git||tobias/rust-sdk-crypto"

        for ver in ["0.9.6"]:
            self.targets[ver] = "https://github.com/quotient-im/libQuotient/archive/%s.tar.gz" % ver
            self.archiveNames[ver] = "libQuotient-%s.tar.gz" % ver
            self.targetInstSrc[ver] = "libQuotient-%s" % ver

        self.targetDigests["0.9.6"] = (["67a286a36343b9b3a02e95d52985f8042aee70f8a12a7513b9f5cb68e1a85721"], CraftHash.HashAlgorithm.SHA256)

        self.defaultTarget = "0.9.6"
        self.description = "A Qt library to write cross-platform clients for Matrix"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/qt/qtbase"] = None

        self.runtimeDependencies["qt-libs/qtkeychain"] = None

        if self.buildTarget == "rust":
            self.runtimeDependencies["libs/corrosion"] = None
        else:
            self.runtimeDependencies["libs/olm"] = None


class Package(CMakePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
