import info
from Blueprints.CraftPackageObject import CraftPackageObject


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()

        self.description = "KGuiAddons"

        self.patchToApply["6.22.0"] = [("wayland-pre-1-23-fix.patch", 1)]
        self.patchLevel["6.22.0"] = 1

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
