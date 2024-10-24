import info
from CraftCore import CraftCore
from CraftOS.osutils import OsUtils
from Package.AutoToolsPackageBase import AutoToolsPackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["3.0.1"]:
            self.targets[ver] = f"https://www.gnupg.org/ftp/gcrypt/libassuan/libassuan-{ver}.tar.bz2"
            self.targetInstSrc[ver] = f"libassuan-{ver}"

        self.targetDigests["3.0.1"] = (["c8f0f42e6103dea4b1a6a483cb556654e97302c7465308f58363778f95f194b1"], CraftHash.HashAlgorithm.SHA256)
        self.patchToApply["3.0.1"] = ("0001-Remove-an-declaration-for-an-unused-function.patch", 1)

        self.description = "An IPC library used by some of the other GnuPG related packages"
        self.defaultTarget = "3.0.1"

    def setDependencies(self):
        self.buildDependencies["dev-utils/msys"] = None
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/gpg-error"] = None


class Package(AutoToolsPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def postInstall(self):
        return self.patchInstallPrefix(
            [self.installDir() / "bin/libassuan-config"],
            OsUtils.toMSysPath(self.subinfo.buildPrefix),
            OsUtils.toMSysPath(CraftCore.standardDirs.craftRoot()),
        )
