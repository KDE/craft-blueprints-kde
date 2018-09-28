import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()

        self.description = "Analitza Library"

        for ver in ['17.08.3']:
            self.patchToApply[ver] = [("0001-Remove-unneeded-type-conversion.patch", 1)]

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.buildDependencies["kde/frameworks/extra-cmake-modules"] = None
        self.runtimeDependencies["libs/qt5/qtbase"] = None

        self.buildDependencies["libs/eigen3"] = None
        self.runtimeDependencies["libs/glew"] = None


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
