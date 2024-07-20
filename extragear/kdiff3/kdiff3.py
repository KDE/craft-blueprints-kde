import os

import info
from CraftCore import CraftCore
from Package.CMakePackageBase import CMakePackageBase
from Packager.AppxPackager import AppxPackager


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()
        # Warning: Craft by default takes the display name to also be the product name.
        self.displayName = "KDiff3"
        self.description = "Compares and merges 2 or 3 files or directories"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/qt6/qt5compat"] = None
        self.buildDependencies["kde/frameworks/extra-cmake-modules"] = None
        self.buildDependencies["libs/boost/boost-headers"] = None
        self.runtimeDependencies["libs/qt/qtbase"] = None
        self.runtimeDependencies["kde/frameworks/tier1/ki18n"] = None
        self.runtimeDependencies["kde/frameworks/tier2/kcrash"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kiconthemes"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kparts"] = None


class Package(CMakePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subinfo.options.configure.args += ["-DBUILD_WITH_QT6=ON"]

    def createPackage(self):
        self.addExecutableFilter(r"bin/(?!(kdiff3|kbuildsycoca5|update-mime-database|kioworker|QtWebEngineProcess)).*")
        self.blacklist_file.append(self.blueprintDir() / "blacklist.txt")
        if CraftCore.compiler.isMacOS:
            self.blacklist_file.append(os.path.join(self.blueprintDir(), "blacklist_mac.txt"))

        self.defines["executable"] = r"bin\kdiff3.exe"
        self.defines["icon"] = os.path.join(self.blueprintDir(), "kdiff3.ico")
        self.defines["alias"] = self.defines["executable"]
        
        self.ignoredPackages.append("binary/mysql")
        # Only attempt to install shell extention in standalone mode
        if not isinstance(self, AppxPackager):
            self.defines["version"] = self.subinfo.buildTarget

            with open(os.path.join(self.blueprintDir(), "sections.nsi")) as file:
                self.defines["sections"] = file.read()

            with open( os.path.join(self.blueprintDir(), "appunistall.nsi"), 'r') as file:
                self.defines["un_sections"] = file.read()
        
        return super().createPackage()
