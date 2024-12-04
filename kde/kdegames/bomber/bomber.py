import info
from Package.CMakePackageBase import CMakePackageBase


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()

        self.description = "Bomber game"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.buildDependencies["kde/frameworks/extra-cmake-modules"] = None
        self.runtimeDependencies["libs/qt/qtbase"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kconfig"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kcoreaddons"] = None
        self.runtimeDependencies["kde/frameworks/tier1/ki18n"] = None
        self.runtimeDependencies["kde/frameworks/tier2/kcrash"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kdbusaddons"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kxmlgui"] = None
        self.runtimeDependencies["kde/kdegames/libkdegames"] = None
        self.runtimeDependencies["kde/plasma/breeze"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kiconthemes"] = None


class Package(CMakePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def createPackage(self):
        self.blacklist_file.append(self.blueprintDir() / "blacklist.txt")
        self.defines["alias"] = "bomber"
        self.defines["icon_png"] = self.blueprintDir() / "150-apps-bomber.png"
        self.defines["icon_png_44"] = self.blueprintDir() / "44-apps-bomber.png"
        self.defines["shortcuts"] = [{"name": "Bomber", "target": "bin/bomber.exe", "description": self.subinfo.description}]
        return super().createPackage()
