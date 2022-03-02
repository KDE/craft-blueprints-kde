import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/qt6/qtbase"] = None
        self.runtimeDependencies["libs/qt6/qtshadertools"] = None

from Blueprints.CraftPackageObject import CraftPackageObject

class Package(CraftPackageObject.get('libs/qt6').pattern):
    def __init__(self):
        CraftPackageObject.get('libs/qt6').pattern.__init__(self)
