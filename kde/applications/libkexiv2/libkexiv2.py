import info


class subinfo(info.infoclass):
    def registerOptions(self):
        if CraftCore.compiler.isMinGW():
            self.parent.package.categoryInfo.compiler = CraftCore.compiler.Compiler.NoCompiler

    def setTargets(self):
        self.versionInfo.setDefaultValues()

        self.description = "Libkexiv2 is a wrapper around Exiv2 library to manipulate pictures metadata as EXIF IPTC and XMP."

    def setDependencies(self):
        self.runtimeDependencies["libs/exiv2"] = None
        self.runtimeDependencies["kde/frameworks/extra-cmake-modules"] = None


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
