import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()

        self.description = "A collection of plugins to handle mobipocket files"

    def setDependencies(self):
        self.buildDependencies["virtual/base"] = None
        self.buildDependencies["kde/frameworks/extra-cmake-modules"] = None
        self.runtimeDependencies["libs/qt/qtbase"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kio"] = None


from Blueprints.CraftPackageObject import CraftPackageObject


class Package(CraftPackageObject.get("kde").pattern):
    def __init__(self):
        super().__init__()
