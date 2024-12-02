import info
from Blueprints.CraftPackageObject import CraftPackageObject
from CraftCore import CraftCore


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()
        self.displayName = "Blinken"
        self.description = "Blinken brings a retro electronic memory game from the 1970's to kde."

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.buildDependencies["kde/frameworks/extra-cmake-modules"] = None
        self.runtimeDependencies["libs/qt/qtbase"] = None
        self.runtimeDependencies["kde/frameworks/tier1/ki18n"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kxmlgui"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kiconthemes"] = None

        if CraftCore.compiler.platform.isAndroid:
            self.runtimeDependencies["kde/frameworks/tier1/kirigami"] = None
            self.runtimeDependencies["kde/unreleased/kirigami-addons"] = None
            self.runtimeDependencies["libs/qt6/qtmultimedia"] = None

        if not CraftCore.compiler.platform.isAndroid:
            self.runtimeDependencies["kde/frameworks/tier2/kdoctools"] = None
            self.runtimeDependencies["kde/frameworks/tier2/kcrash"] = None
            self.runtimeDependencies["kde/frameworks/tier1/kdbusaddons"] = None
            self.runtimeDependencies["qt-libs/phonon"] = None


class Package(CraftPackageObject.get("kde").pattern):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subinfo.options.dynamic.buildTests = False

    def createPackage(self):
        self.defines["appname"] = "blinken"
        self.blacklist_file.append(self.blueprintDir() / "blacklist.txt")
        self.defines["shortcuts"] = [{"name": "Blinken", "target": "bin/blinken.exe", "description": self.subinfo.description}]
        return super().createPackage()
