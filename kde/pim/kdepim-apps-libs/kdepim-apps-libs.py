import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()

        self.description = "KDEPIM-apps library"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = "default"
        self.buildDependencies["kde/frameworks/extra-cmake-modules"] = "default"
        self.runtimeDependencies["libs/qt5/qtbase"] = "default"
        self.runtimeDependencies["kdesupport/grantlee"] = "default"
        self.runtimeDependencies["kde/frameworks/tier1/ki18n"] = "default"
        self.runtimeDependencies["kde/frameworks/tier1/kconfig"] = "default"
        self.runtimeDependencies["kde/frameworks/tier3/kiconthemes"] = "default"
        self.runtimeDependencies["kde/frameworks/tier3/kio"] = "default"
        self.runtimeDependencies["kde/frameworks/tier3/kservice"] = "default"
        self.runtimeDependencies["kde/frameworks/tier1/kwidgetsaddons"] = "default"

        self.runtimeDependencies["kde/pim/akonadi"] = "default"
        self.runtimeDependencies["kde/pim/akonadi-contacts"] = "default"
        self.runtimeDependencies["kde/pim/kcontacts"] = "default"
        self.runtimeDependencies["kde/pim/grantleetheme"] = "default"
        self.runtimeDependencies["kde/pim/libkleo"] = "default"
        self.runtimeDependencies["kde/pim/pimcommon"] = "default"
        self.runtimeDependencies["kdesupport/grantlee"] = "default"


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
