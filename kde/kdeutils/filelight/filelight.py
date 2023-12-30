import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()

        self.description = "GUI utility to show where your diskspace is being used"
        self.displayName = "Filelight"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.buildDependencies["kde/frameworks/extra-cmake-modules"] = None
        self.runtimeDependencies["libs/qt/qtbase"] = None
        self.runtimeDependencies["libs/qt/qtdeclarative"] = None
        self.runtimeDependencies["libs/qt5/qtquickcontrols2"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kirigami"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kquickcharts"] = None
        self.runtimeDependencies["kde/frameworks/tier2/kdoctools"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kdeclarative"] = None
        self.runtimeDependencies["kde/frameworks/tier1/ki18n"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kio"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kxmlgui"] = None
        self.runtimeDependencies["kdesupport/kdewin"] = None
        self.runtimeDependencies["kde/frameworks/tier1/breeze-icons"] = None
        self.runtimeDependencies["kde/frameworks/tier3/qqc2-desktop-style"] = None


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
        self.blacklist_file.append(os.path.join(os.path.dirname(__file__), "blacklist.txt"))

    def createPackage(self):
        self.defines["website"] = "https://apps.kde.org/filelight/"
        self.defines["executable"] = "bin\\filelight.exe"

        # filelight icons
        self.defines["icon"] = os.path.join(self.blueprintDir(), "filelight.ico")
        self.defines["icon_png"] = os.path.join(self.blueprintDir(), ".assets", "150-apps-filelight.png")
        self.defines["icon_png_44"] = os.path.join(self.blueprintDir(), ".assets", "44-apps-filelight.png")

        self.ignoredPackages.append("binary/mysql")

        return TypePackager.createPackage(self)
