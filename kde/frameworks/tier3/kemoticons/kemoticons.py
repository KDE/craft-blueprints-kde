import info
from Blueprints.CraftPackageObject import CraftPackageObject
from CraftCore import CraftCore


class subinfo(info.infoclass):
    def registerOptions(self):
        if not CraftPackageObject.get("libs/qt").instance.subinfo.options.dynamic.qtMajorVersion == "5":
            # Removed in KDE Frameworks 6
            self.parent.package.categoryInfo.compiler = CraftCore.compiler.Compiler.NoCompiler

    def setTargets(self):
        self.versionInfo.setDefaultValues()

        self.description = "Support for emoticons and emoticons themes"

    def setDependencies(self):
        self.buildDependencies["virtual/base"] = None
        self.buildDependencies["kde/frameworks/extra-cmake-modules"] = None
        self.runtimeDependencies["kde/frameworks/tier1/karchive"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kconfig"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kservice"] = None


class Package(CraftPackageObject.get("kde/frameworks").pattern):
    def __init__(self):
        super().__init__()
