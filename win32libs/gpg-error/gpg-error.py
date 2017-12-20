import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.addCachedAutotoolsBuild(f"https://files.kde.org/craft/autotools/mingw_{CraftCore.compiler.bits}/gcc/Release/", "autotools/gpg-error-src")
        self.shortDescription = "Small library with error codes and descriptions shared by most GnuPG related software"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = "default"
        if CraftCore.compiler.isGCCLike():
            self.runtimeDependencies["autotools/gpg-error-src"] = "default"
        else:
            self.runtimeDependencies["win32libs/mingw-crt4msvc"] = "default"


from Package.BinaryPackageBase import *
from Package.MaybeVirtualPackageBase import *


class BinPackage(BinaryPackageBase):
    def __init__(self, **args):
        BinaryPackageBase.__init__(self)


class Package(MaybeVirtualPackageBase):
    def __init__(self):
        MaybeVirtualPackageBase.__init__(self, not CraftCore.compiler.isGCCLike(), classA=BinPackage)
