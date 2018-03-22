import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()

        self.description = "Crypto library"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = "default"
        self.buildDependencies["kde/frameworks/extra-cmake-modules"] = "default"
        self.runtimeDependencies["libs/qt5/qtbase"] = "default"
        self.runtimeDependencies["kde/frameworks/tier1/ki18n"] = "default"
        self.runtimeDependencies["kde/frameworks/tier1/kconfig"] = "default"
        self.runtimeDependencies["kde/frameworks/tier2/kcompletion"] = "default"
        self.runtimeDependencies["kde/frameworks/tier1/kwidgetsaddons"] = "default"
        self.runtimeDependencies["kde/frameworks/tier1/kcoreaddons"] = "default"
        self.runtimeDependencies["kde/frameworks/tier1/kcodecs"] = "default"
        self.runtimeDependencies["kde/frameworks/tier1/kitemmodels"] = "default"
        self.runtimeDependencies["kde/pim/kpimtextedit"] = "default"
        self.runtimeDependencies["libs/gpgme"] = "default"
        self.runtimeDependencies["libs/boost/boost-atomic"] = "default"


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
