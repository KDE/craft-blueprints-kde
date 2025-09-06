import os
import shutil

import info
from CraftCore import CraftCore
from Package.BinaryPackageBase import BinaryPackageBase
from Package.VirtualPackageBase import VirtualPackageBase


class subinfo(info.infoclass):
    def setTargets(self):
        for version in ["3.1.1"]:
            self.targets[version] = "https://archive.apache.org/dist/xerces/c/3/binaries/xerces-c-3.1.1-x86-windows-vc-10.0.zip"
        self.targetDigests["3.1.1"] = "34df759e1ffe4acce301887007cccb62f9496ea0"

        self.description = "A Validating XML Parser"
        self.defaultTarget = "3.1.1"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.buildDependencies["libs/xerces-c"] = None


class PackageBin(BinaryPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subinfo.options.package.withCompiler = False
        self.subinfo.options.package.withSources = False

    def unpack(self):
        if not super().unpack():
            return False
        os.renames(os.path.join(self.sourceDir(), "xerces-c-3.1.1-x86-windows-vc-10.0", "include"), os.path.join(self.sourceDir(), "include"))
        os.renames(os.path.join(self.sourceDir(), "xerces-c-3.1.1-x86-windows-vc-10.0", "bin"), os.path.join(self.sourceDir(), "bin"))
        os.renames(os.path.join(self.sourceDir(), "xerces-c-3.1.1-x86-windows-vc-10.0", "lib"), os.path.join(self.sourceDir(), "lib"))
        shutil.rmtree(os.path.join(self.sourceDir(), "xerces-c-3.1.1-x86-windows-vc-10.0"))
        return True


if CraftCore.compiler.compiler.isMSVC:

    class Package(PackageBin):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)

else:

    class Package(VirtualPackageBase):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)
