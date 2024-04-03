import info
from Blueprints.CraftPackageObject import CraftPackageObject


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()

        self.description = "KWordquiz"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.buildDependencies["kde/frameworks/extra-cmake-modules"] = None
        self.runtimeDependencies["libs/qt/qtbase"] = None
        self.runtimeDependencies["qt-libs/phonon"] = None

        self.runtimeDependencies["kde/frameworks/tier1/ki18n"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kconfig"] = None
        self.runtimeDependencies["kde/frameworks/tier2/kdoctools"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kguiaddons"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kiconthemes"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kitemviews"] = None
        self.runtimeDependencies["kde/frameworks/tier3/knewstuff"] = None
        self.runtimeDependencies["kde/frameworks/tier3/knotifyconfig"] = None
        self.runtimeDependencies["kde/frameworks/tier3/knotifications"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kxmlgui"] = None
        self.runtimeDependencies["kde/applications/libkeduvocdocument"] = None
        self.runtimeDependencies["kde/plasma/breeze"] = None
        if CraftPackageObject.get("libs/qt").instance.subinfo.options.dynamic.qtMajorVersion == "6":
            self.runtimeDependencies["kde/unreleased/kirigami-addons"] = None


class Package(CraftPackageObject.get("kde").pattern):
    def __init__(self):
        super().__init__()

    def createPackage(self):
        self.defines["executable"] = r"bin\kwordquiz.exe"
        self.addExecutableFilter(r"(bin|libexec)/(?!(kwordquiz)).*")
        self.ignoredPackages.append("binary/mysql")
        self.ignoredPackages.append("libs/dbus")
        return super().createPackage()
