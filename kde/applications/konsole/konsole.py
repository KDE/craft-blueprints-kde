import info
from Blueprints.CraftPackageObject import CraftPackageObject
from CraftCore import CraftCore


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()

        self.displayName = "Konsole"
        self.description = "the KDE terminal emulator"
        # Fix macOS build, see https://invent.kde.org/utilities/konsole/-/merge_requests/950
        self.patchToApply["24.02.1"] = [("950.patch", 1)]

    def setDependencies(self):
        self.buildDependencies["virtual/base"] = None
        self.buildDependencies["kde/frameworks/extra-cmake-modules"] = None
        self.buildDependencies["libs/qt/qtbase"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kconfig"] = None
        self.runtimeDependencies["kde/frameworks/tier2/kdoctools"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kguiaddons"] = None
        self.runtimeDependencies["kde/frameworks/tier1/ki18n"] = None
        self.runtimeDependencies["kde/frameworks/tier2/kjobwidgets"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kio"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kparts"] = None
        self.runtimeDependencies["kde/frameworks/tier3/ktexteditor"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kwindowsystem"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kxmlgui"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kdbusaddons"] = None
        self.runtimeDependencies["kde/frameworks/tier2/kpty"] = None
        self.runtimeDependencies["kde/frameworks/tier3/knotifyconfig"] = None
        self.runtimeDependencies["kde/frameworks/tier3/knewstuff"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kglobalaccel"] = None
        self.runtimeDependencies["kde/plasma/breeze"] = None


class Package(CraftPackageObject.get("kde").pattern):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def createPackage(self):
        self.addExecutableFilter(r"(bin|libexec)/(?!(.*/)*(konsole|update-mime-database|kioslave|kdeinit5)).*")
        if CraftCore.compiler.isMacOS:
            self.blacklist_file.append(self.blueprintDir() / "excludelist.txt")

        self.defines["shortcuts"] = [{"name": "Konsole", "target": "bin/konsole.exe", "description": self.subinfo.description}]
        return super().createPackage()
