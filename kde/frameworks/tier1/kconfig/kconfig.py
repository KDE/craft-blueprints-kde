import info
from CraftCore import CraftCore


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()

        if CraftCore.compiler.isWindows:
            self.patchToApply["5.99.0"] = [("fix-window-size.patch", 1)]
            self.patchToApply["5.100.0"] = [("fix-window-size.patch", 1)]
            self.patchLevel["5.99.0"] = 1

        self.description = "KConfig"

    def setDependencies(self):
        self.buildDependencies["virtual/base"] = None
        self.buildDependencies["kde/frameworks/extra-cmake-modules"] = None
        self.runtimeDependencies["libs/qt/qtbase"] = None
        self.buildDependencies["libs/qt/qttools"] = None


from Blueprints.CraftPackageObject import CraftPackageObject

class Package(CraftPackageObject.get('kde').pattern):
    def __init__(self):
        CraftPackageObject.get('kde').pattern.__init__(self)
