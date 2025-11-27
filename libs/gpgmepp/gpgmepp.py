import info
from Package.CMakePackageBase import CMakePackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["2.0.0"]:
            self.targetInstSrc[ver] = f"gpgmepp-{ver}"
            self.targets[ver] = f"https://www.gnupg.org/ftp/gcrypt/gpgmepp/gpgmepp-{ver}.tar.xz"
        self.svnTargets["master"] = "git://git.gnupg.org/gpgmepp.git"
        self.targetDigests["2.0.0"] = (["d4796049c06708a26f3096f748ef095347e1a3c1e570561701fe952c3f565382"], CraftHash.HashAlgorithm.SHA256)
        self.defaultTarget = "2.0.0"
        self.description = "GnuPG cryptography support library (runtime) for C++"

    def setDependencies(self):
        self.runtimeDependencies["libs/assuan2"] = None
        self.runtimeDependencies["libs/gpg-error"] = None
        self.runtimeDependencies["libs/gpgme"] = None
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/gnupg"] = None


class Package(CMakePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
