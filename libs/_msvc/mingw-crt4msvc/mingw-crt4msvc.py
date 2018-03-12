import info


class subinfo( info.infoclass ):
    def setTargets( self ):
        self.addCachedAutotoolsBuild(f"https://files.kde.org/craft/libs/2018.02/windows/mingw_{CraftCore.compiler.bits}/gcc/Release/", "libs/runtime")

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = "default"

from Package.BinaryPackageBase import *

class Package(BinaryPackageBase):
    def __init__(self, **args):
        BinaryPackageBase.__init__(self)
