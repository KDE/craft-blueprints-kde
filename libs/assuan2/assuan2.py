import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.addCachedAutotoolsBuild(f"https://files.kde.org/craft/autotools/2018.02/windows/mingw_{CraftCore.compiler.bits}/gcc/Release/", "autotools/assuan2-src")

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = "default"
        if CraftCore.compiler.isGCCLike():
            self.runtimeDependencies["autotools/assuan2-src"] = "default"
        else:
            self.runtimeDependencies["libs/mingw-crt4msvc"] = "default"
            self.runtimeDependencies["libs/gpg-error"] = "default"


from Package.BinaryPackageBase import *
from Package.MaybeVirtualPackageBase import *


class BinPackage(BinaryPackageBase):
    def __init__(self, **args):
        BinaryPackageBase.__init__(self)


class Package(MaybeVirtualPackageBase):
    def __init__(self):
        MaybeVirtualPackageBase.__init__(self, not CraftCore.compiler.isGCCLike(), classA=BinPackage)
