import info
from Blueprints.CraftPackageObject import CraftPackageObject
from CraftCore import CraftCore


class subinfo(info.infoclass):
    def registerOptions(self):
        if CraftPackageObject.get("libs/qt").instance.subinfo.options.dynamic.qtMajorVersion == "6":
            # Moved from KF5 to Plasma 6
            self.parent.package.categoryInfo.compiler = CraftCore.compiler.Compiler.NoCompiler
        else:
            self.parent.package.categoryInfo.platforms = CraftCore.compiler.Platforms.NotWindows & CraftCore.compiler.Platforms.NotMacOS

    def setTargets(self):
        self.versionInfo.setDefaultValues()
        self.description = "A library for accessing the usage data collected by the activities system"

    def setDependencies(self):
        self.buildDependencies["virtual/base"] = None
        self.buildDependencies["kde/frameworks/extra-cmake-modules"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kconfig"] = None
        self.runtimeDependencies["kde/frameworks/tier2/kactivities"] = None
        self.runtimeDependencies["libs/boost/boost-headers"] = None


class Package(CraftPackageObject.get("kde/frameworks").pattern):
    def __init__(self):
        super().__init__()
