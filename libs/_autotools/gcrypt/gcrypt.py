import info
from Package.AutoToolsPackageBase import AutoToolsPackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["1.10.2"]:
            self.targets[ver] = f"https://gnupg.org/ftp/gcrypt/libgcrypt/libgcrypt-{ver}.tar.bz2"
            self.targetInstSrc[ver] = f"libgcrypt-{ver}"
            self.patchToApply[ver] = ("fix-getrandom-mac.diff", 1)
        self.targetDigests["1.10.2"] = (["3b9c02a004b68c256add99701de00b383accccf37177e0d6c58289664cce0c03"], CraftHash.HashAlgorithm.SHA256)

        self.description = " General purpose crypto library based on the code used in GnuPG."
        self.defaultTarget = "1.10.2"

    def setDependencies(self):
        self.buildDependencies["dev-utils/msys"] = None
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/gpg-error"] = None


class Package(AutoToolsPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subinfo.options.configure.args += ["--disable-static", "--enable-shared", "--disable-asm", "--disable-padlock-support"]
