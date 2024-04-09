import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.addCachedAutotoolsBuild("libs/_autotools/assuan2")

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/mingw-crt4msvc"] = None
        self.runtimeDependencies["libs/gpg-error"] = None


from Package.BinaryPackageBase import *
from Package.MaybeVirtualPackageBase import *


class Package(BinaryPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
