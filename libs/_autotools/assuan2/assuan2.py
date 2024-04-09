import info


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["2.5.5"]:
            self.targets[ver] = f"https://www.gnupg.org/ftp/gcrypt/libassuan/libassuan-{ver}.tar.bz2"
            self.targetInstSrc[ver] = f"libassuan-{ver}"

        self.targetDigests["2.5.5"] = (["8e8c2fcc982f9ca67dcbb1d95e2dc746b1739a4668bc20b3a3c5be632edb34e4"], CraftHash.HashAlgorithm.SHA256)

        self.description = "An IPC library used by some of the other GnuPG related packages"
        self.defaultTarget = "2.5.5"

    def setDependencies(self):
        self.buildDependencies["dev-utils/msys"] = None
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/gpg-error"] = None


from Package.AutoToolsPackageBase import *


class Package(AutoToolsPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def postInstall(self):
        return self.patchInstallPrefix(
            [os.path.join(self.installDir(), "bin", "libassuan-config")],
            OsUtils.toMSysPath(self.subinfo.buildPrefix),
            OsUtils.toMSysPath(CraftCore.standardDirs.craftRoot()),
        )
