import info
from CraftCore import CraftCore
from Package.CMakePackageBase import CMakePackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def registerOptions(self):
        if CraftCore.compiler.isMinGW():
            # Theoretically qgpgme supports mingw but the cmake patches are incomplete
            self.parent.package.categoryInfo.compiler = CraftCore.compiler.Compiler.NoCompiler

    def setTargets(self):
        for ver in ["2.0.0"]:
            self.targets[ver] = f"https://gnupg.org/ftp/gcrypt/qgpgme/qgpgme-{ver}.tar.xz"
            self.targetInstSrc[ver] = f"qgpgme-{ver}"

        self.targetDigests["2.0.0"] = (["15645b2475cca6118eb2ed331b3a8d9442c9d4019c3846ba3f6d25321b4a61ad"], CraftHash.HashAlgorithm.SHA256)
        if CraftCore.compiler.isMSVC():
            self.patchToApply["2.0.0"] = [
                ("msvc.patch", 1),
                ("0001-Workaround-compile-errors-with-MSVC-2022.patch", 1),
            ]

        self.defaultTarget = "2.0.0"

    def setDependencies(self):
        self.runtimeDependencies["libs/assuan2"] = None
        self.runtimeDependencies["libs/gpg-error"] = None
        self.runtimeDependencies["libs/gpgme/gpgme"] = None
        self.runtimeDependencies["libs/gpgme/gpgmepp"] = None
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/gnupg"] = None
        self.runtimeDependencies["libs/qt/qtbase"] = None


class Package(CMakePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subinfo.options.configure.args += ["-DBUILD_WITH_QT5=OFF"]
