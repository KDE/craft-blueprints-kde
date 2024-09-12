import info
from Blueprints.CraftPackageObject import CraftPackageObject


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()

        self.description = "KGuiAddons"

        # Android statusbar recoloring
        # See https://invent.kde.org/frameworks/kguiaddons/-/merge_requests/119
        self.patchToApply["6.5.0"] = ("android-statusbar.diff", 1)
        self.patchLevel["6.5.0"] = 1

    def setDependencies(self):
        self.buildDependencies["virtual/base"] = None
        self.buildDependencies["kde/frameworks/extra-cmake-modules"] = None
        self.runtimeDependencies["libs/qt/qtbase"] = None
        self.runtimeDependencies["libs/qt/qtwayland"] = None
        self.runtimeDependencies["kde/libs/plasma-wayland-protocols"] = None


class Package(CraftPackageObject.get("kde/frameworks").pattern):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
