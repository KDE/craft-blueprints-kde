import info
from CraftCore import CraftCore
from Package.CMakePackageBase import CMakePackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def registerOptions(self):
        if CraftCore.compiler.isMinGW():
            # Theoretically gpgmepp supports mingw but the cmake patches are incomplete
            self.parent.package.categoryInfo.compiler &= CraftCore.compiler.Compiler.NoCompiler

    def setTargets(self):
        self.versionInfo.setDefaultValues()
        self.targetDigests["1.23.2"] = (["9499e8b1f33cccb6815527a1bc16049d35a6198a6c5fae0185f2bd561bce5224"], CraftHash.HashAlgorithm.SHA256)
        self.patchToApply["1.23.2"] = [
            ("cmake.patch", 1),
            ("gpgmepp-1.21.0-20231109.diff", 1),
        ]
        if CraftCore.compiler.isMSVC():
            self.patchToApply["1.23.2"] += [
                ("0001-Workaround-compile-errors-with-MSVC-2022.patch", 1),
            ]

    def setDependencies(self):
        self.runtimeDependencies["libs/assuan2"] = None
        self.runtimeDependencies["libs/gpg-error"] = None
        self.runtimeDependencies["libs/gpgme/gpgme"] = None
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/gnupg"] = None
        self.runtimeDependencies["libs/qt/qtbase"] = None


class Package(CMakePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subinfo.options.configure.args += ["-DWITH_QT=ON"]
        self.subinfo.options.configure.args += ["-DQGPGME_BUILD_QT5=OFF"]
