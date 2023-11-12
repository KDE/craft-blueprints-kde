import info
from Blueprints.CraftPackageObject import CraftPackageObject


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()
        # https://invent.kde.org/frameworks/kcoreaddons/-/merge_requests/327
        for ver in ["5.106.0"]:
            self.patchToApply[ver] = [("327.patch", 1)]
        self.description = "KCoreAddons"

    def setDependencies(self):
        self.buildDependencies["virtual/base"] = None
        self.buildDependencies["kde/frameworks/extra-cmake-modules"] = None
        self.runtimeDependencies["libs/qt/qtbase"] = None
        self.runtimeDependencies["libs/shared-mime-info"] = None


class Package(CraftPackageObject.get("kde/frameworks").pattern):
    def __init__(self):
        super().__init__()
