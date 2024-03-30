import info
from Blueprints.CraftVersion import CraftVersion


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()
        self.description = "Project Management"
        self.webpage = "https://calligra.org/plan"

    def setDependencies(self):
        self.buildDependencies["dev-utils/pkg-config"] = None
        self.runtimeDependencies["libs/qt/qtbase"] = None
        self.runtimeDependencies["kdesupport/qca"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kholidays"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kconfig"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kcoreaddons"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kdbusaddons"] = None
        self.runtimeDependencies["kde/frameworks/tier1/ki18n"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kitemviews"] = None
        self.runtimeDependencies["kde/frameworks/tier1/threadweaver"] = None
        self.runtimeDependencies["kde/frameworks/tier1/breeze-icons"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kguiaddons"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kwidgetsaddons"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kwindowsystem"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kitemmodels"] = None
        self.runtimeDependencies["kde/frameworks/tier1/karchive"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kcalendarcore"] = None
        self.runtimeDependencies["kde/frameworks/tier2/kjobwidgets"] = None
        self.runtimeDependencies["kde/plasma/plasma-activities"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kconfigwidgets"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kiconthemes"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kcmutils"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kio"] = None
        self.runtimeDependencies["kde/frameworks/tier3/knotifications"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kparts"] = None
        self.runtimeDependencies["kde/frameworks/tier3/ktextwidgets"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kwallet"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kxmlgui"] = None
        self.runtimeDependencies["extragear/kdiagram"] = None

        if CraftCore.compiler.isMinGW():
            self.runtimeDependencies["libs/runtime"] = None  # mingw-based builds need this


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self):
        super().__init__()
        self.subinfo.options.dynamic.buildTests = False

    def createPackage(self):
        self.defines["shortcuts"] = [
            {"name": "Calligra Plan", "target": "bin/calligraplan.exe"},
            {"name": "Calligra Plan Work", "target": "bin/calligraplanwork.exe"},
            {"name": "Calligra Plan Portfolio", "target": "bin/calligraplanportfolio.exe"},
        ]
        self.blacklist_file.append(self.blueprintDir() / "blacklist.txt")

        self.ignoredPackages.append("binary/mysql")

        return super().createPackage()
