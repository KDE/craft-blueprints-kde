import info
from CraftCore import CraftCore
from Package.AutoToolsPackageBase import AutoToolsPackageBase
from Package.VirtualPackageBase import VirtualPackageBase


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["3.1.1"]:
            self.targets[ver] = f"https://archive.apache.org/dist/xerces/c/3/sources/xerces-c-{ver}.tar.gz"
            self.targetInstSrc[ver] = f"xerces-c-{ver}"
        self.targetDigests["3.1.1"] = "177ec838c5119df57ec77eddec9a29f7e754c8b2"

        self.description = "A Validating XML Parser"
        self.defaultTarget = "3.1.1"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        if CraftCore.compiler.isMSVC():
            self.buildDependencies["binary/xerces-c-bin"] = None


class PackageMSys(AutoToolsPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


if CraftCore.compiler.isMinGW():

    class Package(PackageMSys):
        pass

else:

    class Package(VirtualPackageBase):
        pass
