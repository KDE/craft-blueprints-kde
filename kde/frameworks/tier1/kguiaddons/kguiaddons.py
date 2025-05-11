import info
from Blueprints.CraftPackageObject import CraftPackageObject


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()

        self.description = "KGuiAddons"

    def setDependencies(self):
        self.buildDependencies["virtual/base"] = None
        self.buildDependencies["kde/frameworks/extra-cmake-modules"] = None
        self.runtimeDependencies["libs/qt/qtbase"] = None
        self.runtimeDependencies["libs/qt/qtdeclarative"] = None
        self.runtimeDependencies["libs/qt/qtwayland"] = None
        self.runtimeDependencies["kde/libs/plasma-wayland-protocols"] = None
        self.runtimeDependencies["libs/wayland-protocols"] = None


class Package(CraftPackageObject.get("kde/frameworks").pattern):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
