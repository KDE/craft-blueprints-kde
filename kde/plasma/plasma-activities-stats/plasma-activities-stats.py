import info
from Blueprints.CraftPackageObject import CraftPackageObject
from CraftCore import CraftCore


class subinfo(info.infoclass):
    def registerOptions(self):
        self.parent.package.categoryInfo.platforms &= ~CraftCore.compiler.Platforms.Windows & ~CraftCore.compiler.Platforms.MacOS

    def setTargets(self):
        self.versionInfo.setDefaultValues()
        self.description = "A library for accessing the usage data collected by the activities system"

    def setDependencies(self):
        self.buildDependencies["virtual/base"] = None
        self.buildDependencies["kde/frameworks/extra-cmake-modules"] = None
        self.runtimeDependencies["kde/plasma/plasma-activities"] = None
        if self.options.dynamic.buildTests:
            self.runtimeDependencies["libs/boost"] = None


class Package(CraftPackageObject.get("kde/plasma").pattern):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
