import info
from Blueprints.CraftPackageObject import CraftPackageObject


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()

    def setDependencies(self):
        self.buildDependencies["libs/qt6/qttools"] = None
        self.runtimeDependencies["libs/qt6/qtbase"] = None


class Package(CraftPackageObject.get("libs/qt6").pattern):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
