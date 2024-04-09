import info
from Blueprints.CraftPackageObject import CraftPackageObject
from CraftCore import CraftCore


class subinfo(info.infoclass):
    def registerOptions(self):
        # would need somone who cares
        self.parent.package.categoryInfo.platforms = CraftCore.compiler.Platforms.NotWindows & CraftCore.compiler.Platforms.NotMacOS

    def setTargets(self):
        self.versionInfo.setDefaultValues()

        self.description = "Baloo is a file indexing and searching framework."

    def setDependencies(self):
        self.runtimeDependencies["libs/qt/qtbase"] = None
        self.runtimeDependencies["kde/frameworks/tier1/solid"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kconfig"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kcoreaddons"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kdbusaddons"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kidletime"] = None
        self.runtimeDependencies["kde/frameworks/tier2/kfilemetadata"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kio"] = None
        self.runtimeDependencies["libs/lmdb"] = None


class Package(CraftPackageObject.get("kde/frameworks").pattern):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
