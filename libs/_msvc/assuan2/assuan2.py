import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.addCachedAutotoolsBuild(f"https://files.kde.org/craft/autotools/2018.02/windows/mingw_{CraftCore.compiler.bits}/gcc/Release/", "autotools/assuan2-src")

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = "default"
        self.runtimeDependencies["libs/mingw-crt4msvc"] = "default"
        self.runtimeDependencies["libs/gpg-error"] = "default"


from Package.BinaryPackageBase import *
from Package.MaybeVirtualPackageBase import *


class Package(BinaryPackageBase):
    def __init__(self, **args):
        BinaryPackageBase.__init__(self)
