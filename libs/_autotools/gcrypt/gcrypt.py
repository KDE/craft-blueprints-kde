import info
from Package.AutoToolsPackageBase import AutoToolsPackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["1.11.0"]:
            self.targets[ver] = f"https://gnupg.org/ftp/gcrypt/libgcrypt/libgcrypt-{ver}.tar.bz2"
            self.targetInstSrc[ver] = f"libgcrypt-{ver}"
        self.targetDigests["1.11.0"] = (["09120c9867ce7f2081d6aaa1775386b98c2f2f246135761aae47d81f58685b9c"], CraftHash.HashAlgorithm.SHA256)

        self.description = " General purpose crypto library based on the code used in GnuPG."
        self.defaultTarget = "1.11.0"

    def setDependencies(self):
        self.buildDependencies["dev-utils/msys"] = None
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/gpg-error"] = None


class Package(AutoToolsPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subinfo.options.configure.args += ["--disable-static", "--enable-shared", "--disable-asm", "--disable-padlock-support"]
