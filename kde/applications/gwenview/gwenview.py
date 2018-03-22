import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()

        self.description = "Gwenview is a fast and easy to use image viewer for KDE."

    def setDependencies(self):
        self.buildDependencies["virtual/base"] = "default"
        self.buildDependencies["kde/frameworks/extra-cmake-modules"] = "default"
        self.buildDependencies["libs/qt5/qtbase"] = "default"
        self.runtimeDependencies["libs/libjpeg-turbo"] = "default"
        self.runtimeDependencies["libs/libpng"] = "default"
        self.runtimeDependencies["libs/exiv2"] = "default"
        self.runtimeDependencies["libs/lcms2"] = "default"
        self.runtimeDependencies["kde/libs/libkdcraw"] = "default"
        self.runtimeDependencies["kde/frameworks/tier3/kactivities"] = "default"
        self.runtimeDependencies["kde/frameworks/tier4/kdelibs4support"] = "default"
        self.runtimeDependencies["qt-libs/phonon"] = "default"


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
