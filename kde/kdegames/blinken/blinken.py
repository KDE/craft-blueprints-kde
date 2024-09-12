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
        
        if CraftCore.compiler.isAndroid:
            self.runtimeDependencies["kde/frameworks/tier1/kirigami"] = None
            self.runtimeDependencies["kde/unreleased/kirigami-addons"] = None
            self.runtimeDependencies["libs/qt6/qtmultimedia"] = None
    
        if not CraftCore.compiler.isAndroid:
            self.runtimeDependencies["kde/frameworks/tier2/kdoctools"] = None
            self.runtimeDependencies["kde/frameworks/tier2/kcrash"] = None
            self.runtimeDependencies["kde/frameworks/tier1/kdbusaddons"] = None
            self.runtimeDependencies["qt-libs/phonon"] = None


class Package(CraftPackageObject.get("kde").pattern):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def createPackage(self):

        self.defines["appname"] = "blinken"

        # Finally, just call the packager itself to get the package actually created.
        return super().createPackage()