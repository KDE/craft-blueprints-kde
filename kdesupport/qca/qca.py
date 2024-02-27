import info


class subinfo(info.infoclass):
    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/qt/qtbase"] = None
        self.runtimeDependencies["libs/openssl"] = None

        # gcrypt currently fails to build for android
        if not CraftCore.compiler.isAndroid:
            self.runtimeDependencies["libs/gcrypt"] = None

        # cyrus-sasl currently fails to build with mingw / for android
        if not CraftCore.compiler.isMinGW() and not CraftCore.compiler.isAndroid:
            self.runtimeDependencies["libs/cyrus-sasl"] = None

        if CraftPackageObject.get("libs/qt").instance.subinfo.options.dynamic.qtMajorVersion == "6":
            self.runtimeDependencies["libs/qt6/qt5compat"] = None


    def setTargets(self):
        self.description = "Qt Cryptographic Architecture (QCA)"

        self.svnTargets["master"] = "https://anongit.kde.org/qca.git"

        for ver in ["2.3.7"]:
            self.targets[ver] = f"https://download.kde.org/stable/qca/{ver}/qca-{ver}.tar.xz"
            self.targetDigests[ver] = (["fee2343b54687d5be3e30fb33ce296ee50ac7ae5e23d7ab725f63ffdf7af3f43"], CraftHash.HashAlgorithm.SHA256)
            self.targetInstSrc[ver] = f"qca-{ver}"

        # latest stable version
        self.defaultTarget = "2.3.7"


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self, **args):
        super().__init__()

        # tests fail to build with missing openssl header
        self.subinfo.options.configure.args = ["-DBUILD_TESTS=OFF"]

        if CraftPackageObject.get("libs/qt").instance.subinfo.options.dynamic.qtMajorVersion == "6":
            self.subinfo.options.configure.args += ["-DBUILD_WITH_QT6=ON"]
