import info
from Package.MesonPackageBase import MesonPackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def setTargets(self):
        self.description = "C library for the Public Suffix List"
        self.webpage = "C library for the Public Suffix List "

        for ver in ["0.21.5"]:
            self.targets[ver] = f"https://github.com/rockdaboot/libpsl/releases/download/{ver}/libpsl-{ver}.tar.gz"
            self.targetInstSrc[ver] = f"libpsl-{ver}"
        self.targetDigests["0.21.5"] = (["1dcc9ceae8b128f3c0b3f654decd0e1e891afc6ff81098f227ef260449dae208"], CraftHash.HashAlgorithm.SHA256)
        self.defaultTarget = "0.21.5"

    def setDependencies(self):
        self.buildDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/gettext"] = None
        self.runtimeDependencies["libs/icu"] = None


class Package(MesonPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
