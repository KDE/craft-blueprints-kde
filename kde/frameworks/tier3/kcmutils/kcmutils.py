import info
from Blueprints.CraftPackageObject import CraftPackageObject
from CraftCore import CraftCore


class subinfo(info.infoclass):
    def registerOptions(self):
        self.parent.package.categoryInfo.platforms = CraftCore.compiler.Platforms.NotAndroid

    def setTargets(self):
        self.versionInfo.setDefaultValues()

        self.description = "Extra API to write KConfigModules"

    def setDependencies(self):
        self.buildDependencies["virtual/base"] = None
        self.buildDependencies["kde/frameworks/extra-cmake-modules"] = None
        self.runtimeDependencies["libs/qt/qtbase"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kcoreaddons"] = None
        self.runtimeDependencies["kde/frameworks/tier1/ki18n"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kitemviews"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kxmlgui"] = None
        if CraftPackageObject.get("libs/qt").instance.subinfo.options.dynamic.qtMajorVersion == "5":
            self.runtimeDependencies["kde/frameworks/tier3/kconfigwidgets"] = None
            self.runtimeDependencies["kde/frameworks/tier3/kdeclarative"] = None
            self.runtimeDependencies["kde/frameworks/tier3/kservice"] = None
            self.runtimeDependencies["kde/frameworks/tier3/kiconthemes"] = None

        if CraftPackageObject.get("libs/qt").instance.subinfo.options.dynamic.qtMajorVersion == "6":
            self.runtimeDependencies["kde/frameworks/tier1/kirigami"] = None
            self.runtimeDependencies["kde/frameworks/tier2/kactivities"] = None
            self.runtimeDependencies["kde/frameworks/tier3/kio"] = None
            self.runtimeDependencies["kde/frameworks/tier2/kpackage"] = None


class Package(CraftPackageObject.get("kde/frameworks").pattern):
    def __init__(self):
        super().__init__()
