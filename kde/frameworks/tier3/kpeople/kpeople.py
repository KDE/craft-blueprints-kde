import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()

        self.description = "Unified access to our contacts from different sources"

        self.patchToApply["5.82.0"] = [("0001-Fix-DBus-check.patch", 1)]
        self.patchLevel["5.82.0"] = 1

        self.patchToApply["5.83.0"] = [("0001-Add-find_dependency-for-QtWidgets.patch", 1)]
        self.patchLevel["5.83.0"] = 1

    def setDependencies(self):
        self.buildDependencies["virtual/base"] = None
        self.buildDependencies["kde/frameworks/extra-cmake-modules"] = None
        self.runtimeDependencies["libs/qt5/qtbase"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kitemviews"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kwidgetsaddons"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kcoreaddons"] = None

from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
