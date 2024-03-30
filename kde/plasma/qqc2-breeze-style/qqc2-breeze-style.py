import info
from Blueprints.CraftPackageObject import CraftPackageObject
from CraftCore import CraftCore


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()

    def setDependencies(self):
        self.runtimeDependencies["libs/qt/qtbase"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kcoreaddons"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kirigami"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kconfig"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kguiaddons"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kquickcharts"] = None
        self.runtimeDependencies["kde/frameworks/tier2/kcolorscheme"] = None

        if not CraftCore.compiler.isAndroid:
            self.runtimeDependencies["kde/frameworks/tier3/kiconthemes"] = None


class Package(CraftPackageObject.get("kde/plasma").pattern):
    def __init__(self):
        super().__init__()
