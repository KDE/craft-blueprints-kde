import os

import info
from Blueprints.CraftPackageObject import CraftPackageObject
from Package.CMakePackageBase import CMakePackageBase


class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets["master"] = "https://invent.kde.org/pim/ktimetracker.git|master"
        self.defaultTarget = "5.0.1"

        for ver in ["5.0.0", "5.0.1"]:
            self.targets[ver] = f"https://download.kde.org/stable/ktimetracker/{ver}/src/ktimetracker-{ver}.tar.xz"
            self.targetInstSrc[ver] = f"ktimetracker-{ver}"

        self.displayName = "KTimeTracker"
        self.description = "Personal Time Tracker"
        self.webpage = "https://userbase.kde.org/KTimeTracker"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.buildDependencies["kde/frameworks/extra-cmake-modules"] = None
        self.runtimeDependencies["libs/qt/qtbase"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kcalendarcore"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kconfig"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kdbusaddons"] = None
        self.runtimeDependencies["kde/frameworks/tier1/ki18n"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kidletime"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kwindowsystem"] = None
        self.runtimeDependencies["kde/frameworks/tier2/kdoctools"] = None
        self.runtimeDependencies["kde/frameworks/tier2/kjobwidgets"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kconfigwidgets"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kio"] = None
        self.runtimeDependencies["kde/frameworks/tier3/knotifications"] = None
        self.runtimeDependencies["kde/frameworks/tier3/ktextwidgets"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kxmlgui"] = None
        self.runtimeDependencies["kde/frameworks/tier2/kstatusnotifieritem"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kcmutils"] = None
        # KTimeTracker forces Breeze style on Windows
        self.runtimeDependencies["kde/plasma/breeze"] = None


class Package(CMakePackageBase):
    def __init__(self):
        super().__init__()

    def createPackage(self):
        self.defines["productname"] = "KTimeTracker"
        self.defines["website"] = "https://userbase.kde.org/KTimeTracker"
        self.defines["executable"] = "bin\\ktimetracker.exe"
        self.defines["icon"] = os.path.join(self.blueprintDir(), "ktimetracker.ico")

        self.blacklist_file.append(self.blueprintDir() / "blacklist.txt")

        return super().createPackage()
