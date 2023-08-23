import info
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets["master"] = "https://github.com/quotient-im/libQuotient.git||dev"

        for ver in ["0.8.1"]:
            self.targets[ver] = "https://github.com/quotient-im/libQuotient/archive/%s.tar.gz" % ver
            self.archiveNames[ver] = "libQuotient-%s.tar.gz" % ver
            self.targetInstSrc[ver] = "libQuotient-%s" % ver

        self.targetDigests["0.8.1"] = (["7786d7b8f46d64577f885234951d79aae2ba6823d8d2ba98acbde102fa1b43b1"], CraftHash.HashAlgorithm.SHA256)

        self.defaultTarget = "0.8.1"
        self.description = "A Qt library to write cross-platform clients for Matrix"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/qt/qtbase"] = None
        if CraftPackageObject.get("libs/qt").instance.subinfo.options.dynamic.qtMajorVersion == "5":
            # Yes, this is correct :-) QtMultimedia is only a dependency with Qt5 for libQuotient
            # See https://github.com/quotient-im/libQuotient/issues/483
            self.runtimeDependencies["libs/qt5/qtmultimedia"] = None

        self.runtimeDependencies["qt-libs/qtkeychain"] = None
        self.runtimeDependencies["libs/olm"] = None


class Package(CMakePackageBase):
    def __init__(self, **args):
        CMakePackageBase.__init__(self)
        # LINK : fatal error LNK1104: cannot open file 'Quotient.lib
        # And fixes crash on android
        self.subinfo.options.dynamic.buildStatic = True
        self.subinfo.options.configure.args = "-DQuotient_ENABLE_E2EE=ON"
        if CraftPackageObject.get("libs/qt").instance.subinfo.options.dynamic.qtMajorVersion == "6":
            self.subinfo.options.configure.args = "-DBUILD_WITH_QT6=1"
