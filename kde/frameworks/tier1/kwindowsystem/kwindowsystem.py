import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()

        self.description = "KWindowSystem"
        self.patchToApply["5.93.0"] = [("0001-5.93-android-support.diff", 1)]

    def setDependencies(self):
        self.buildDependencies["virtual/base"] = None
        self.buildDependencies["kde/frameworks/extra-cmake-modules"] = None
        self.runtimeDependencies["libs/qt5/qtbase"] = None
        if OsUtils.isUnix():
            self.runtimeDependencies["libs/qt5/qtx11extras"] = None
        else:
            self.runtimeDependencies["libs/qt5/qtwinextras"] = None


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
