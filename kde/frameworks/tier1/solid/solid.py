import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()

        if CraftCore.compiler.isLinux:
            self.patchToApply["5.81.0"] = [("fix-solid-compile.diff", 1)]
            self.patchToApply["5.82.0"] = [("fix-solid-compile.diff", 1)]
            self.patchLevel["5.81.0"] = 1

        self.description = "Solid"

    def setDependencies(self):
        self.buildDependencies["virtual/base"] = None
        self.buildDependencies["kde/frameworks/extra-cmake-modules"] = None
        self.runtimeDependencies["libs/qt5/qtbase"] = None
        self.runtimeDependencies["libs/qt5/qtdeclarative"] = None


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
