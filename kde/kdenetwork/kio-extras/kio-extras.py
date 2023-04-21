import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()
        self.patchLevel["22.12.3"] = 1

        self.description = "Extra plugins for KIO (thumbnail generators, archives, remote filesystems and more)"

    def setDependencies(self):
        self.buildDependencies["virtual/base"] = None
        self.buildDependencies["kde/frameworks/extra-cmake-modules"] = None
        self.runtimeDependencies["libs/libssh"] = None
        self.runtimeDependencies["libs/openexr"] = None
        self.runtimeDependencies["libs/taglib"] = None
        self.runtimeDependencies["libs/qt5/qtbase"] = None
        self.runtimeDependencies["kde/frameworks/tier2/kactivities"] = None
        self.runtimeDependencies["kde/frameworks/tier1/karchive"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kbookmarks"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kconfig"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kconfigwidgets"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kcoreaddons"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kdbusaddons"] = None
        self.runtimeDependencies["kde/frameworks/tier2/kdoctools"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kguiaddons"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kiconthemes"] = None
        self.runtimeDependencies["kde/frameworks/tier1/ki18n"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kio"] = None
        self.runtimeDependencies["kde/frameworks/tier1/solid"] = None
        self.runtimeDependencies["kde/frameworks/tier2/kdnssd"] = None
        self.runtimeDependencies["kde/frameworks/tier1/syntax-highlighting"] = None
        self.runtimeDependencies["kde/applications/libkexiv2"] = None

from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
