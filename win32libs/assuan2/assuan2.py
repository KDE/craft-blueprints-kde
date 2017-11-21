import info


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["2.4.3"]:
            self.targets[ver] = f"https://files.kde.org/craft/3rdparty/gpgme/mingw_{CraftCore.compiler.bits}/gcc/Release/assuan2-src-{ver}-windows-mingw_{CraftCore.compiler.bits}-gcc.7z"
            self.targetDigestUrls[ver] = f"{self.targets[ver]}.sha256"

        self.shortDescription = "An IPC library used by some of the other GnuPG related packages"
        self.defaultTarget = "2.4.3"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = "default"
        if CraftCore.compiler.isGCCLike():
            self.runtimeDependencies["autotools/assuan2-src"] = "default"
        else:
            self.runtimeDependencies["win32libs/mingw-crt4msvc"] = "default"
            self.runtimeDependencies["win32libs/gpg-error"] = "default"


from Package.BinaryPackageBase import *
from Package.MaybeVirtualPackageBase import *


class BinPackage(BinaryPackageBase):
    def __init__(self, **args):
        BinaryPackageBase.__init__(self)


class Package(MaybeVirtualPackageBase):
    def __init__(self):
        MaybeVirtualPackageBase.__init__(self, not CraftCore.compiler.isGCCLike(), classA=BinPackage)
