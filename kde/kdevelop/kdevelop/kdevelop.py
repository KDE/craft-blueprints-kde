import os
import subprocess
import sys

import info
from Blueprints.CraftPackageObject import CraftPackageObject
from Blueprints.CraftVersion import CraftVersion
from CraftCore import CraftCore
from info import DependencyRequirementType


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()
        self.description = "KDE Integrated Development Environment for C/C++/QML/JS/Python/PHP/..."
        self.webpage = "https://kdevelop.org"
        self.displayName = "KDevelop"

    def registerOptions(self):
        self.options.dynamic.registerOption("fullKDevelop", False)
        self.options.dynamic.registerOption("fullPlasma", False)

    def setDependencies(self):
        self.buildDependencies["virtual/base"] = None
        self.buildDependencies["kde/frameworks/extra-cmake-modules"] = None
        self.buildDependencies["dev-utils/7zip"] = None
        self.buildDependencies["libs/boost"] = None
        self.runtimeDependencies["libs/llvm"] = None
        self.runtimeDependencies["libs/qt/qtbase"] = None
        self.runtimeDependencies["libs/qt/qtdeclarative"] = None
        self.runtimeDependencies["libs/qt/qtwebengine"] = None
        self.runtimeDependencies["kde/frameworks/tier1/breeze-icons"] = None
        self.runtimeDependencies["kde/frameworks/tier1/karchive"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kconfig"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kguiaddons"] = None
        self.runtimeDependencies["kde/frameworks/tier1/ki18n"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kiconthemes"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kitemmodels"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kitemviews"] = None
        self.runtimeDependencies["kde/frameworks/tier2/kjobwidgets"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kcmutils"] = None
        self.runtimeDependencies["kde/frameworks/tier3/knewstuff"] = None
        self.runtimeDependencies["kde/frameworks/tier3/knotifyconfig"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kparts"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kservice"] = None
        self.runtimeDependencies["kde/frameworks/tier1/sonnet"] = None
        self.runtimeDependencies["kde/frameworks/tier3/ktexteditor"] = None
        self.runtimeDependencies["kde/frameworks/tier1/threadweaver"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kwindowsystem"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kxmlgui"] = None
        self.runtimeDependencies["kde/kdesdk/libkomparediff2"] = None
        self.runtimeDependencies["kde/frameworks/tier1/ktexttemplate"] = None
        self.runtimeDependencies["data/hicolor-icon-theme"] = None

        if self.options.dynamic.fullPlasma:
            self.runtimeDependencies["kde/frameworks/tier3/krunner"] = None
            self.runtimeDependencies["kde/plasma/libplasma"] = None
        if self.options.dynamic.fullKDevelop:
            self.packagingDependencies["kde/kdevelop/kdev-python"] = None
            self.packagingDependencies["kde/kdevelop/kdev-php"] = None
        self.runtimeDependencies["extragear/kdevelop-pg-qt"] = None

        # Install extra plugins shipped by Kate
        self.runtimeDependencies["kde/applications/kate"] = None


class Package(CraftPackageObject.get("kde").pattern):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def preArchive(self):
        installColorSchemesScript = os.path.join(self.sourceDir(), "release-scripts/install_colorschemes.py")
        CraftCore.log.info(f"Executing: {installColorSchemesScript}")
        subprocess.check_call([sys.executable, installColorSchemesScript, os.path.join(self.archiveDir(), "bin/data")])
        return super().preArchive()

    def createPackage(self):
        # TODO re-enable exclude list
        # self.blacklist_file.append(self.blueprintDir() / "blacklist.txt")
        # self.whitelist_file.append(self.blueprintDir() / "whitelist.txt")

        self.defines["shortcuts"] = [
            {"name": "KDevelop", "target": "bin/kdevelop.exe"},
            {"name": "KDevelop - Microsoft Visual C++ compiler", "target": "bin/kdevelop-msvc.bat"},
        ]
        self.defines["icon"] = self.blueprintDir() / "kdevelop.ico"

        self.ignoredPackages.append("binary/mysql")

        return super().createPackage()
