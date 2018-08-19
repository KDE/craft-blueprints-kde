import info
from Package.BinaryPackageBase import *


class subinfo(info.infoclass):
    def setTargets(self):
        self.targets["0.29.2"] = "http://repo.msys2.org/mingw/x86_64/mingw-w64-x86_64-pkg-config-0.29.2-1-any.pkg.tar.xz"
        self.targetDigests["0.28"] = "8fe89c3ac4217beffbb942a2e9da3597d30226e8"
        self.targetInstSrc["0.29.2"] = "mingw64"
        self.targetInstallPath["0.29.2"] = "dev-utils"
        self.defaultTarget = "0.29.2"

    def setDependencies(self):
        self.buildDependencies["virtual/bin-base"] = "default"
        self.buildDependencies["libs/mingw-crt4msvc"] = "default"


class Package(BinaryPackageBase):
    def __init__(self):
        BinaryPackageBase.__init__(self)
