import info
from Blueprints.CraftPackageObject import CraftPackageObject


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
        if CraftPackageObject.get("libs/qt").instance.subinfo.options.dynamic.qtMajorVersion == "6":
            self.runtimeDependencies["kde/unreleased/kirigami-addons"] = None


class Package(CraftPackageObject.get("kde").pattern):
    def __init__(self):
        super().__init__()

    def createPackage(self):
        self.blacklist_file.append(self.blueprintDir() / "blacklist.txt")
        self.addExecutableFilter(r"bin/(?!(filelight|update-mime-database|kioslave)).*")
        self.defines["website"] = "https://apps.kde.org/filelight/"
        self.defines["executable"] = "bin\\filelight.exe"

        # filelight icons
        self.defines["icon"] = self.blueprintDir() / "filelight.ico"
        self.defines["icon_png"] = self.blueprintDir() / ".assets/150-apps-filelight.png"
        self.defines["icon_png_44"] = self.blueprintDir() / ".assets/44-apps-filelight.png"

        self.ignoredPackages.append("binary/mysql")

        return super().createPackage()
