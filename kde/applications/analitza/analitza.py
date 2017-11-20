import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()

        self.description = "Analitza Library"

        for ver in ['17.08.3']:
            self.patchToApply[ver] = [("0001-Remove-unneeded-type-conversion.patch", 1)]

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = "default"
        self.buildDependencies["frameworks/extra-cmake-modules"] = "default"
        self.runtimeDependencies["libs/qt5/qtbase"] = "default"

        self.buildDependencies["win32libs/eigen3"] = "default"
        self.runtimeDependencies["win32libs/glew"] = "default"


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
