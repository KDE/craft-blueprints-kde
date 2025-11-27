import info
from Package.CMakePackageBase import CMakePackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["2.0.0"]:
            self.targetInstSrc[ver] = f"qgpgme-{ver}"
            self.targets[ver] = f"https://www.gnupg.org/ftp/gcrypt/qgpgme/qgpgme-{ver}.tar.xz"
        self.svnTargets["master"] = "git://git.gnupg.org/qgpgme.git"
        self.targetDigests["2.0.0"] = (["15645b2475cca6118eb2ed331b3a8d9442c9d4019c3846ba3f6d25321b4a61ad"], CraftHash.HashAlgorithm.SHA256)
        self.defaultTarget = "2.0.0"
        self.description = "GnuPG cryptography support library (runtime) for Qt"

    def setDependencies(self):
        self.runtimeDependencies["libs/assuan2"] = None
        self.runtimeDependencies["libs/gpg-error"] = None
        self.runtimeDependencies["libs/gpgme"] = None
        self.runtimeDependencies["libs/gpgmepp"] = None
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/gnupg"] = None
        self.runtimeDependencies["libs/qt/qtbase"] = None


class Package(CMakePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
