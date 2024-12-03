import info
from Blueprints.CraftPackageObject import CraftPackageObject


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()

        self.description = "KDEgames Library"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.buildDependencies["kde/frameworks/extra-cmake-modules"] = None
        self.runtimeDependencies["libs/qt/qtbase"] = None
        self.runtimeDependencies["libs/libsndfile"] = None
        self.runtimeDependencies["libs/openal-soft"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kcoreaddons"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kconfig"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kwidgetsaddons"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kcodecs"] = None
        self.runtimeDependencies["kde/frameworks/tier1/karchive"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kdbusaddons"] = None
        self.runtimeDependencies["kde/frameworks/tier1/ki18n"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kguiaddons"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kitemviews"] = None
        self.runtimeDependencies["kde/frameworks/tier2/kcompletion"] = None
        self.runtimeDependencies["kde/frameworks/tier3/ktextwidgets"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kxmlgui"] = None
        self.runtimeDependencies["kde/frameworks/tier2/kcrash"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kio"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kbookmarks"] = None
        self.runtimeDependencies["kde/frameworks/tier2/kdnssd"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kdeclarative"] = None
        self.runtimeDependencies["kde/frameworks/tier3/knewstuff"] = None


class Package(CraftPackageObject.get("kde").pattern):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def createPackage(self):
        self.blacklist_file.append(self.blueprintDir() / "blacklist.txt")
        self.defines["shortcuts"] = [{"name": "Libkdegames", "target": "bin/libkdegames.exe", "description": self.subinfo.description}]
        return super().createPackage()
