import info
from Package.AutoToolsPackageBase import AutoToolsPackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["1.11.2"]:
            self.targets[ver] = f"https://gnupg.org/ftp/gcrypt/libgcrypt/libgcrypt-{ver}.tar.bz2"
            self.targetInstSrc[ver] = f"libgcrypt-{ver}"
        self.targetDigests["1.11.2"] = (["6ba59dd192270e8c1d22ddb41a07d95dcdbc1f0fb02d03c4b54b235814330aac"], CraftHash.HashAlgorithm.SHA256)

        self.description = " General purpose crypto library based on the code used in GnuPG."
        self.defaultTarget = "1.11.2"

    def setDependencies(self):
        self.buildDependencies["dev-utils/msys"] = None
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/gpg-error"] = None


class Package(AutoToolsPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subinfo.options.configure.args += ["--disable-asm", "--disable-padlock-support"]
