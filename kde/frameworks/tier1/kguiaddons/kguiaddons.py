import info
from Blueprints.CraftPackageObject import CraftPackageObject


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()

        self.description = "KGuiAddons"

        # Fix Android with Qt 6.8
        # See https://invent.kde.org/frameworks/kguiaddons/-/merge_requests/146
        # Fix possible crash in case QDBus reply error
        # See https://invent.kde.org/frameworks/kguiaddons/-/merge_requests/147
        self.patchToApply["6.7.0"] = [("146.patch", 1), ("147.patch", 1)]
        self.patchLevel["6.7.0"] = 1

        self.patchToApply["6.8.0"] = [("147.patch", 1)]
        self.patchLevel["6.8.0"] = 1

    def setDependencies(self):
        self.buildDependencies["virtual/base"] = None
        self.buildDependencies["kde/frameworks/extra-cmake-modules"] = None
        self.runtimeDependencies["libs/qt/qtbase"] = None
        self.runtimeDependencies["libs/qt/qtdeclarative"] = None
        self.runtimeDependencies["libs/qt/qtwayland"] = None
        self.runtimeDependencies["kde/libs/plasma-wayland-protocols"] = None


class Package(CraftPackageObject.get("kde/frameworks").pattern):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
