import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()

        self.description = "KWalletManager"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = "default"
        self.buildDependencies["kde/frameworks/extra-cmake-modules"] = "default"
        self.runtimeDependencies["libs/qt5/qtbase"] = "default"
        self.runtimeDependencies["kde/frameworks/tier1/karchive"] = "default"
        self.runtimeDependencies["kde/frameworks/tier2/kauth"] = "default"
        self.runtimeDependencies["kde/frameworks/tier1/kconfig"] = "default"
        self.runtimeDependencies["kde/frameworks/tier1/kdbusaddons"] = "default"
        self.runtimeDependencies["kde/frameworks/tier2/kdoctools"] = "default"
        self.runtimeDependencies["kde/frameworks/tier1/ki18n"] = "default"
        self.runtimeDependencies["kde/frameworks/tier3/kiconthemes"] = "default"
        self.runtimeDependencies["kde/frameworks/tier2/kjobwidgets"] = "default"
        self.runtimeDependencies["kde/frameworks/tier3/kcmutils"] = "default"
        self.runtimeDependencies["kde/frameworks/tier3/kio"] = "default"
        self.runtimeDependencies["kde/frameworks/tier3/knotifications"] = "default"
        self.runtimeDependencies["kde/frameworks/tier3/kservice"] = "default"
        self.runtimeDependencies["kde/frameworks/tier3/ktextwidgets"] = "default"
        self.runtimeDependencies["kde/frameworks/tier3/kwallet"] = "default"
        self.runtimeDependencies["kde/frameworks/tier1/kwindowsystem"] = "default"
        self.runtimeDependencies["kde/frameworks/tier3/kxmlgui"] = "default"


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
