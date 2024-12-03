import info
from Package.CMakePackageBase import CMakePackageBase


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()

        self.description = "Picmi"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.buildDependencies["kde/frameworks/extra-cmake-modules"] = None
        self.runtimeDependencies["libs/qt/qtbase"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kconfig"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kcoreaddons"] = None
        self.runtimeDependencies["kde/frameworks/tier2/kcrash"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kdbusaddons"] = None
        self.runtimeDependencies["kde/frameworks/tier2/kdoctools"] = None
        self.runtimeDependencies["kde/frameworks/tier3/knewstuff"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kxmlgui"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kiconthemes"] = None
        self.runtimeDependencies["kde/kdegames/libkdegames"] = None


class Package(CMakePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def createPackage(self):
        self.blacklist_file.append(self.blueprintDir() / "blacklist.txt")
        self.defines["alias"] = ["picmi"]
        self.defines["icon"] = self.blueprintDir() / "picmi.ico"
        self.defines["icon_png"] = self.blueprintDir() / "150-apps-picmi.png"
        self.defines["icon_png_44"] = self.blueprintDir() / "44-apps-picmi.png"
        self.defines["shortcuts"] = [{"name": "Picmi", "target": "bin/picmi.exe", "description": self.subinfo.description}]
        return super().createPackage()
