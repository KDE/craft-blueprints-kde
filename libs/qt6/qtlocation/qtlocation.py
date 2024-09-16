import info
from Blueprints.CraftPackageObject import CraftPackageObject


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()

        # https://codereview.qt-project.org/c/qt/qtlocation/+/604697
        self.patchToApply["6.8.0"] = [("qtlocation-stuck-tile-provider-fix.diff", 1)]
        self.patchLevel["6.8.0"] = 1
        self.patchToApply["6.8.1"] = [("qtlocation-stuck-tile-provider-fix.diff", 1)]

    def setDependencies(self):
        self.runtimeDependencies["libs/qt6/qtbase"] = None
        self.runtimeDependencies["libs/qt6/qtdeclarative"] = None
        self.runtimeDependencies["libs/qt6/qtpositioning"] = None


class Package(CraftPackageObject.get("libs/qt6").pattern):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
