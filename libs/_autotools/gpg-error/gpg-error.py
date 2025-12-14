import info
from CraftCore import CraftCore
from CraftOS.osutils import OsUtils
from Package.AutoToolsPackageBase import AutoToolsPackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["1.56"]:
            self.targets[ver] = f"https://www.gnupg.org/ftp/gcrypt/libgpg-error/libgpg-error-{ver}.tar.bz2"
            self.targetInstSrc[ver] = f"libgpg-error-{ver}"

        self.targetDigests["1.56"] = (["82c3d2deb4ad96ad3925d6f9f124fe7205716055ab50e291116ef27975d169c0"], CraftHash.HashAlgorithm.SHA256)

        self.description = "Small library with error codes and descriptions shared by most GnuPG related software"
        self.defaultTarget = "1.56"

    def setDependencies(self):
        self.buildDependencies["dev-utils/msys"] = None
        self.runtimeDependencies["libs/iconv"] = None
        self.runtimeDependencies["virtual/base"] = None


class Package(AutoToolsPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subinfo.options.configure.bootstrap = True
        self.subinfo.options.configure.args += ["--enable-install-gpg-error-config"]

    def postInstall(self):
        return self.patchInstallPrefix(
            [self.installDir() / "bin" / "gpg-error-config", self.installDir() / "bin" / "gpgrt-config"],
            OsUtils.toMSysPath(self.subinfo.buildPrefix),
            OsUtils.toMSysPath(CraftCore.standardDirs.craftRoot()),
        )
