import info
from CraftCore import CraftCore


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues(packageName="breeze-icons")

        self.description = "Install of the actual breeze icon, only supposed to be used on linux to make the icons available for linuxdeploy."

    def registerOptions(self):
        self.parent.package.categoryInfo.platforms = CraftCore.compiler.Platforms.Linux

    def setDependencies(self):
        self.buildDependencies["virtual/base"] = None
        self.buildDependencies["kde/frameworks/extra-cmake-modules"] = None
        self.buildDependencies["python-modules/lxml"] = None
        self.runtimeDependencies["libs/qt5/qtbase"] = None


from Blueprints.CraftPackageObject import CraftPackageObject
from Package.CMakePackageBase import CMakePackageBase
from Package.MaybeVirtualPackageBase import MaybeVirtualPackageBase


class CMakePackage(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)


class Package(MaybeVirtualPackageBase):
    def __init__(self):
        # we skip this package if the icons are already installed
        useRcc = CraftPackageObject.get("kde/frameworks/tier1/breeze-icons").subinfo.options.dynamic.useIconResource
        MaybeVirtualPackageBase.__init__(self, useRcc, classA=CMakePackage)
