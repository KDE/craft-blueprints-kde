import info
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()
        self.description = "Collection management software, free and simple"
        self.displayName = "Tellico"
        self.webpage = "https://tellico-project.org/"

    def setDependencies(self):
        self.buildDependencies["virtual/base"] = None
        self.buildDependencies["kde/frameworks/extra-cmake-modules"] = None
        self.runtimeDependencies["libs/gettext"] = None
        self.runtimeDependencies["libs/qt/qtbase"] = None
        self.runtimeDependencies["kde/frameworks/tier1/karchive"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kcodecs"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kconfig"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kconfigwidgets"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kcoreaddons"] = None
        self.runtimeDependencies["kde/frameworks/tier2/kcrash"] = None
        self.runtimeDependencies["kde/frameworks/tier2/kdoctools"] = None
        self.runtimeDependencies["kde/frameworks/tier2/kfilemetadata"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kguiaddons"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kiconthemes"] = None
        self.runtimeDependencies["kde/frameworks/tier1/ki18n"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kio"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kitemmodels"] = None
        self.runtimeDependencies["kde/frameworks/tier2/kjobwidgets"] = None
        self.runtimeDependencies["kde/frameworks/tier2/kpackage"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kwidgetsaddons"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kwindowsystem"] = None
        self.runtimeDependencies["kde/frameworks/tier1/solid"] = None
        self.runtimeDependencies["kde/frameworks/tier3/knewstuff"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kwallet"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kxmlgui"] = None
        self.runtimeDependencies["libs/shared-mime-info"] = None
        # master (and 3.4) build against qtcharts and qtwebengine (MSVC)
        self.runtimeDependencies["libs/qt/qtcharts"] = None
        if not CraftCore.compiler.isMinGW():
            self.runtimeDependencies["libs/qt/qtwebengine"] = None


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)

    def createPackage(self):
        self.defines["appname"] = "tellico"
        self.defines["website"] = "https://tellico-project.org/"
        self.defines["shortcuts"] = [{"name": self.subinfo.displayName, "target": "bin\\tellico.exe"}]
        self.defines["license"] = os.path.join(self.sourceDir(), "COPYING")
        self.defines["file_types"] = [".tc"]
        self.defines["icon"] = self.buildDir() / "src/ICONS_SOURCES.ico"
        self.ignoredPackages.append("binary/mysql")

        # self.blacklist_file.append(os.path.join(self.blueprintDir(), 'blacklist.txt'))

        return TypePackager.createPackage(self)
