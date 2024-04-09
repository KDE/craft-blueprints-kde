import info
from Blueprints.CraftPackageObject import CraftPackageObject


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()

        self.description = "Plugin based library to create window decorations."

    def setDependencies(self):
        self.buildDependencies["virtual/base"] = None
        self.buildDependencies["kde/frameworks/extra-cmake-modules"] = None
        self.runtimeDependencies["libs/qt/qtbase"] = None
        self.buildDependencies["libs/qt/qttools"] = None


class Package(CraftPackageObject.get("kde/plasma").pattern):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
