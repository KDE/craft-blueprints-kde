import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()

        self.description = "Blogilo"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = "default"
        self.buildDependencies["kde/frameworks/extra-cmake-modules"] = "default"
        self.runtimeDependencies["libs/qt5/qtbase"] = "default"
        self.runtimeDependencies["kde/frameworks/tier1/ki18n"] = "default"
        self.runtimeDependencies["kde/frameworks/tier2/kcrash"] = "default"
        self.runtimeDependencies["kde/frameworks/tier1/kdbusaddons"] = "default"
        self.runtimeDependencies["kde/frameworks/tier2/kdoctools"] = "default"
        self.runtimeDependencies["kde/frameworks/tier3/kwallet"] = "default"
        self.runtimeDependencies["kde/frameworks/tier3/kxmlgui"] = "default"
        self.runtimeDependencies["kde/frameworks/tier1/syntax-highlighting"] = "default"

        self.runtimeDependencies["kde/pim/kblog"] = "default"
        self.runtimeDependencies["kde/pim/pimcommon"] = "default"
        self.runtimeDependencies["kde/pim/kpimtextedit"] = "default"
        self.runtimeDependencies["kde/pim/messagelib"] = "default"
        self.runtimeDependencies["kde/pim/kimap"] = "default"
        self.runtimeDependencies["kde/pim/libkgapi"] = "default"
        self.runtimeDependencies["libs/qt5/qtwebengine"] = "default"


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
