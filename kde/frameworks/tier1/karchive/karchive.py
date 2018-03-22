import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()

        self.description = "Qt 5 addon providing access to numerous types of archives"

    def setDependencies(self):
        self.buildDependencies["virtual/base"] = "default"
        self.buildDependencies["libs/libarchive"] = "default"
        self.buildDependencies["kde/frameworks/extra-cmake-modules"] = "default"
        self.runtimeDependencies["libs/qt5/qtbase"] = "default"
        self.runtimeDependencies["libs/libbzip2"] = "default"
        self.runtimeDependencies["libs/zlib"] = "default"
        if not CraftCore.compiler.isMSVC2010() and not CraftCore.compiler.isMSVC2012():
            self.runtimeDependencies["libs/liblzma"] = "default"


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
