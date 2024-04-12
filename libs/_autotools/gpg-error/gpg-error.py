import info


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["1.47"]:
            self.targets[ver] = f"https://www.gnupg.org/ftp/gcrypt/libgpg-error/libgpg-error-{ver}.tar.bz2"
            self.targetInstSrc[ver] = f"libgpg-error-{ver}"
        self.targetDigests["1.47"] = (["9e3c670966b96ecc746c28c2c419541e3bcb787d1a73930f5e5f5e1bcbbb9bdb"], CraftHash.HashAlgorithm.SHA256)
        self.description = "Small library with error codes and descriptions shared by most GnuPG related software"
        self.defaultTarget = "1.47"

    def setDependencies(self):
        self.buildDependencies["dev-utils/msys"] = None
        self.runtimeDependencies["libs/iconv"] = None
        self.runtimeDependencies["virtual/base"] = None


from Package.AutoToolsPackageBase import *


class Package(AutoToolsPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subinfo.options.configure.bootstrap = True
        self.subinfo.options.configure.args += ["--disable-static", "--enable-shared", "--enable-install-gpg-error-config"]

    def postInstall(self):
        return self.patchInstallPrefix(
            [os.path.join(self.installDir(), "bin", "gpg-error-config"), os.path.join(self.installDir(), "bin", "gpgrt-config")],
            OsUtils.toMSysPath(self.subinfo.buildPrefix),
            OsUtils.toMSysPath(CraftCore.standardDirs.craftRoot()),
        )
