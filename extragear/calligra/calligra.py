import info
from CraftCore import CraftCore
from Package.CMakePackageBase import CMakePackageBase


class subinfo(info.infoclass):
    def setTargets(self):
        # self.versionInfo.setDefaultValues()
        self.svnTargets["master"] = "https://anongit.kde.org/calligra.git"
        self.defaultTarget = "master"
        self.description = "The Integrated Work Applications Suite by KDE"
        self.webpage = "https://calligra.org/"
        self.displayName = "Calligra Gemini"

    def setDependencies(self):
        self.buildDependencies["dev-utils/pkgconf"] = None
        self.runtimeDependencies["libs/qt/qtbase"] = None
        # Qt WebEngine doesn't work with MinGW.
        if not CraftCore.compiler.isMinGW():
            self.runtimeDependencies["libs/qt/qtwebengine"] = None
        self.runtimeDependencies["libs/boost"] = None
        self.runtimeDependencies["libs/lcms2"] = None
        self.runtimeDependencies["libs/libgit2"] = None
        self.runtimeDependencies["libs/eigen3"] = None
        #        self.runtimeDependencies['libs/vc'] = None
        self.runtimeDependencies["kdesupport/qca"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kcodecs"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kconfig"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kcoreaddons"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kdbusaddons"] = None
        self.runtimeDependencies["kde/frameworks/tier1/ki18n"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kitemviews"] = None
        self.runtimeDependencies["kde/frameworks/tier1/sonnet"] = None
        self.runtimeDependencies["kde/frameworks/tier1/threadweaver"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kirigami"] = None
        self.runtimeDependencies["kde/frameworks/tier1/breeze-icons"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kguiaddons"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kwidgetsaddons"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kwindowsystem"] = None
        self.runtimeDependencies["kde/frameworks/tier2/kdoctools"] = None
        self.runtimeDependencies["kde/frameworks/tier2/kcompletion"] = None
        self.runtimeDependencies["kde/frameworks/tier2/kjobwidgets"] = None
        self.runtimeDependencies["kde/plasma/plasma-activities"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kconfigwidgets"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kiconthemes"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kcmutils"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kio"] = None
        self.runtimeDependencies["kde/frameworks/tier3/knotifications"] = None
        self.runtimeDependencies["kde/frameworks/tier3/knotifyconfig"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kparts"] = None
        self.runtimeDependencies["kde/frameworks/tier3/ktextwidgets"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kwallet"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kxmlgui"] = None
        self.runtimeDependencies["extragear/kdiagram"] = None

        if CraftCore.compiler.isMinGW():
            self.runtimeDependencies["libs/runtime"] = None  # mingw-based builds need this


class Package(CMakePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def createPackage(self):
        self.defines["appname"] = "calligragemini"
        self.defines["icon"] = self.sourceDir() / "gemini/calligragemini.ico"
        self.defines["shortcuts"] = [
            {"name": self.subinfo.displayName, "target": "bin/calligragemini.exe"},
            {"name": "Calligra Sheets", "target": "bin/calligrasheets.exe"},
            {"name": "Calligra Words", "target": "bin/calligrawords.exe"},
            {"name": "Calligra Karbon", "target": "bin/karbon.exe"},
        ]
        self.blacklist_file.append(self.blueprintDir() / "blacklist.txt")

        self.ignoredPackages.append("binary/mysql")
        self.ignoredPackages.append("dev-utils/sed")

        return super().createPackage()
