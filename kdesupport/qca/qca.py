import info
from Package.CMakePackageBase import CMakePackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def setTargets(self):
        self.description = "Qt Cryptographic Architecture (QCA)"

        self.svnTargets["master"] = "https://invent.kde.org/libraries/qca.git"

        for ver in ["2.3.7", "2.3.10"]:
            self.targets[ver] = f"https://download.kde.org/stable/qca/{ver}/qca-{ver}.tar.xz"
            self.targetInstSrc[ver] = f"qca-{ver}"
        self.targetDigests["2.3.7"] = (["fee2343b54687d5be3e30fb33ce296ee50ac7ae5e23d7ab725f63ffdf7af3f43"], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests["2.3.10"] = (["1c5b722da93d559365719226bb121c726ec3c0dc4c67dea34f1e50e4e0d14a02"], CraftHash.HashAlgorithm.SHA256)
        self.patchToApply["2.3.10"] = [("qca-2.3.10-20251106.diff", 1)]  # diable messing with pdbs

        self.webpage = "https://invent.kde.org/libraries/qca"
        # latest stable version
        self.defaultTarget = "2.3.10"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/qt/qtbase"] = None
        self.runtimeDependencies["libs/qt6/qt5compat"] = None
        self.runtimeDependencies["libs/openssl"] = None
        self.runtimeDependencies["libs/gcrypt"] = None
        self.runtimeDependencies["libs/cyrus-sasl"] = None
        self.runtimeDependencies["libs/gnupg"] = None


class Package(CMakePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.subinfo.options.configure.args = [
            f"-DBUILD_TESTS={self.subinfo.options.dynamic.buildTests.asOnOff}",
            "-DBUILD_WITH_QT6=ON",
            f"-DWITH_cyrus-sasl_PLUGIN={self.subinfo.options.isActive('libs/cyrus-sasl').asYesNo}",
            f"-DWITH_gcrypt_PLUGIN={self.subinfo.options.isActive('libs/gcrypt').asYesNo}",
            f"-DWITH_gnupg_PLUGIN={self.subinfo.options.isActive('libs/gnupg').asYesNo}",
            f"-DWITH_ossl_PLUGIN={self.subinfo.options.isActive('libs/openssl').asYesNo}",
        ]
