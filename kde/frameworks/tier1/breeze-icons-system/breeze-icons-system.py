import info
from Blueprints.CraftPackageObject import CraftPackageObject
from CraftCore import CraftCore
from Package.MaybeVirtualPackageBase import MaybeVirtualPackageBase


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
        self.runtimeDependencies["libs/qt/qtbase"] = None


class CMakePackage(CraftPackageObject.get("kde/frameworks").pattern):
    def __init__(self):
        super().__init__()


class Package(MaybeVirtualPackageBase):
    def __init__(self):
        # we skip this package if the icons are already installed
        useRcc = CraftPackageObject.get("kde/frameworks/tier1/breeze-icons").subinfo.options.dynamic.useIconResource
        super().__init__(useRcc, classA=CMakePackage)
