import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()

        self.description = "Parley"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = "default"
        self.buildDependencies["kde/frameworks/extra-cmake-modules"] = "default"
        self.runtimeDependencies["libs/qt5/qtbase"] = "default"
        self.runtimeDependencies["libs/qt5/qtmultimedia"] = "default"
        self.runtimeDependencies["libs/qt5/qtwebengine"] = "default"

        self.runtimeDependencies["kde/frameworks/tier2/kdoctools"] = "default"
        self.runtimeDependencies["kde/frameworks/tier1/kcoreaddons"] = "default"
        self.runtimeDependencies["kde/frameworks/tier1/kconfig"] = "default"
        self.runtimeDependencies["kde/frameworks/tier2/kcrash"] = "default"
        self.runtimeDependencies["kde/frameworks/tier1/ki18n"] = "default"
        self.runtimeDependencies["kde/frameworks/tier3/kio"] = "default"
        self.runtimeDependencies["kde/frameworks/tier3/knewstuff"] = "default"
        self.runtimeDependencies["kde/frameworks/tier3/kross"] = "default"
        self.runtimeDependencies["kde/frameworks/tier3/khtml"] = "default"
        self.runtimeDependencies["kde/frameworks/tier1/sonnet"] = "default"
        self.runtimeDependencies["kde/frameworks/tier3/kcmutils"] = "default"
        self.runtimeDependencies["kde/frameworks/tier3/kxmlgui"] = "default"
        self.runtimeDependencies["kde/frameworks/tier3/knotifications"] = "default"
        self.runtimeDependencies["kde/applications/libkeduvocdocument"] = "default"
        self.runtimeDependencies["libs/libxslt"] = "default"
        self.runtimeDependencies["libs/libxml2"] = "default"


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
