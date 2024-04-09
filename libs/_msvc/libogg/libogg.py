import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.addCachedAutotoolsBuild(f"libs/_autotools/{self.parent.package.name}")

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/mingw-crt4msvc"] = None


from Package.BinaryPackageBase import *


class Package(BinaryPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
