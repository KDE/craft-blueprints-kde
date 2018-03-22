import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()

        self.description = "Akregator"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = "default"
        self.buildDependencies["kde/frameworks/extra-cmake-modules"] = "default"
        self.runtimeDependencies["libs/qt5/qtbase"] = "default"
        self.runtimeDependencies["kde/frameworks/tier2/kcrash"] = "default"
        self.runtimeDependencies["kde/frameworks/tier2/kdoctools"] = "default"
        self.runtimeDependencies["kde/frameworks/tier3/kcmutils"] = "default"
        self.runtimeDependencies["kde/frameworks/tier3/knotifications"] = "default"
        self.runtimeDependencies["kde/frameworks/tier3/kiconthemes"] = "default"
        self.runtimeDependencies["kde/frameworks/tier3/kparts"] = "default"
        self.runtimeDependencies["kde/frameworks/tier3/ktexteditor"] = "default"
        self.runtimeDependencies["kde/frameworks/tier3/kxmlgui"] = "default"
        self.runtimeDependencies["kde/frameworks/tier1/kdbusaddons"] = "default"

        self.runtimeDependencies["kde/pim/grantleetheme"] = "default"
        self.runtimeDependencies["kde/pim/kontactinterface"] = "default"
        self.runtimeDependencies["kde/pim/libkdepim"] = "default"
        self.runtimeDependencies["kde/pim/libkleo"] = "default"
        self.runtimeDependencies["kde/pim/messagelib"] = "default"
        self.runtimeDependencies["kde/pim/syndication"] = "default"
        self.runtimeDependencies["kde/pim/akonadi-mime"] = "default"
        self.runtimeDependencies["kde/pim/pimcommon"] = "default"


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
