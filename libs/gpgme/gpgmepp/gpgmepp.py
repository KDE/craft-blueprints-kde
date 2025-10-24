import info
from CraftCore import CraftCore
from Package.CMakePackageBase import CMakePackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def registerOptions(self):
        if CraftCore.compiler.isMinGW():
            # Theoretically gpgmepp supports mingw but the cmake patches are incomplete
            self.parent.package.categoryInfo.compiler = CraftCore.compiler.Compiler.NoCompiler

    def setTargets(self):
        for ver in ["2.0.0"]:
            self.targets[ver] = f"https://gnupg.org/ftp/gcrypt/gpgmepp/gpgmepp-{ver}.tar.xz"
            self.targetInstSrc[ver] = f"gpgmepp-{ver}"

        self.targetDigests["2.0.0"] = (["d4796049c06708a26f3096f748ef095347e1a3c1e570561701fe952c3f565382"], CraftHash.HashAlgorithm.SHA256)
        if CraftCore.compiler.isMSVC():
            self.patchToApply["2.0.0"] = [
                ("msvc.patch", 1),
            ]

        self.defaultTarget = "2.0.0"

    def setDependencies(self):
        self.runtimeDependencies["libs/assuan2"] = None
        self.runtimeDependencies["libs/gpg-error"] = None
        self.runtimeDependencies["libs/gpgme/gpgme"] = None
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/gnupg"] = None


class Package(CMakePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
