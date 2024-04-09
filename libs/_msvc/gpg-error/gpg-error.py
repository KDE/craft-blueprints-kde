import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.addCachedAutotoolsBuild("libs/_autotools/gpg-error")

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/mingw-crt4msvc"] = None


from Package.BinaryPackageBase import *


class Package(BinaryPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
