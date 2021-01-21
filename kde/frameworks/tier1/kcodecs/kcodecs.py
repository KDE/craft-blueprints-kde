import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()
        self.patchToApply["5.78.0"] = [("0001-Remove-the-usage-of-non-UTF-8-string-literals.patch", 1)]
        self.patchLevel["5.78.0"] = 1

        self.description = "Plugins allowing Qt applications to access further types of images"

    def setDependencies(self):
        self.buildDependencies["virtual/base"] = None
        self.buildDependencies["kde/frameworks/extra-cmake-modules"] = None
        self.runtimeDependencies["libs/qt5/qtbase"] = None
        self.buildDependencies["dev-utils/gperf"] = None


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
