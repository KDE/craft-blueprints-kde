import info


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["3.1.1"]:
            self.targets[ver] = "http://archive.apache.org/dist/xerces/c/3/sources/xerces-c-" + ver + ".tar.gz"
            self.targetInstSrc[ver] = "xerces-c-" + ver
        self.targetDigests["3.1.1"] = "177ec838c5119df57ec77eddec9a29f7e754c8b2"

        self.description = "A Validating XML Parser"
        self.defaultTarget = "3.1.1"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        if CraftCore.compiler.isMSVC():
            self.buildDependencies["binary/xerces-c-bin"] = None


from Package.AutoToolsPackageBase import *
from Package.VirtualPackageBase import *


class PackageMSys(AutoToolsPackageBase):
    def __init__(self):
        super().__init__()


if CraftCore.compiler.isMinGW():

    class Package(PackageMSys):
        pass

else:

    class Package(VirtualPackageBase):
        pass
