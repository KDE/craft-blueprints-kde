import info
from Blueprints.CraftPackageObject import CraftPackageObject
from CraftCore import CraftCore


class subinfo(info.infoclass):
    def registerOptions(self):
        self.parent.package.categoryInfo.platforms &= ~CraftCore.compiler.Platforms.Windows & ~CraftCore.compiler.Platforms.MacOS

    def setTargets(self):
        self.versionInfo.setDefaultValues()

    def setDependencies(self):
        self.buildDependencies["virtual/base"] = None
        self.buildDependencies["kde/frameworks/extra-cmake-modules"] = None
        self.runtimeDependencies["libs/qt/qtbase"] = None
        self.runtimeDependencies["libs/qt/qtwayland"] = None
        self.runtimeDependencies["kde/libs/plasma-wayland-protocols"] = None
        self.runtimeDependencies["libs/wayland-protocols"] = None
        self.runtimeDependencies["libs/wayland"] = None


class Package(CraftPackageObject.get("kde/plasma").pattern):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
