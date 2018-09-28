import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.addCachedAutotoolsBuild("libs/_autotools/gpgme")

    def setDependencies(self):
        self.runtimeDependencies['virtual/base'] = 'default'
        self.runtimeDependencies["libs/mingw-crt4msvc"] = None
        self.runtimeDependencies['libs/assuan2'] = 'default'
        self.runtimeDependencies["libs/gpg-error"] = None


from Package.BinaryPackageBase import *
from Package.MaybeVirtualPackageBase import *


class Package(BinaryPackageBase):
    def __init__(self, **args):
        BinaryPackageBase.__init__(self)
