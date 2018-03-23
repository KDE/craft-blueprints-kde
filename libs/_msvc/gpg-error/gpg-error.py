import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.addCachedAutotoolsBuild("libs/_autotools/gpg-error")

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = "default"
        self.runtimeDependencies["libs/mingw-crt4msvc"] = "default"


from Package.BinaryPackageBase import *


class Package(BinaryPackageBase):
    def __init__(self, **args):
        BinaryPackageBase.__init__(self)
