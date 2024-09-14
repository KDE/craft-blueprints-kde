import info
from CraftCore import CraftCore
from Package.AutoToolsPackageBase import AutoToolsPackageBase


class subinfo(info.infoclass):
    def registerOptions(self):
        self.parent.package.categoryInfo.architecture = CraftCore.compiler.architecture.x86

    def setTargets(self):
        self.description = "Autotooled version of the opensource Intel media sdk dispatcher"
        self.svnTargets["61ac4d2"] = "https://github.com/lu-zero/mfx_dispatch.git||61ac4d2ce63d0efc1a5cb37c949ea3ad44dc73e1"
        self.defaultTarget = "61ac4d2"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/libva"] = None


class Package(AutoToolsPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
