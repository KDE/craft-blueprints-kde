import info
from Blueprints.CraftPackageObject import CraftPackageObject


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()

        # Android icon recoloring
        # See https://invent.kde.org/frameworks/kirigami/-/merge_requests/1606
        self.patchToApply["6.5.0"] = ("1606.patch", 1)
        self.patchLevel["6.5.0"] = 1
        self.patchToApply["6.8.0"] = ("fix-stack-actions.patch", 1)
        self.patchLevel["6.8.0"] = 1

    def setDependencies(self):
        self.buildDependencies["virtual/base"] = None
        self.buildDependencies["kde/frameworks/extra-cmake-modules"] = None
        self.runtimeDependencies["libs/qt/qtbase"] = None
        self.runtimeDependencies["libs/qt/qtsvg"] = None
        self.buildDependencies["libs/qt/qttools"] = None


class Package(CraftPackageObject.get("kde/frameworks").pattern):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
