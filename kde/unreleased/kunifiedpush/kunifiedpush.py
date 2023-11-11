import info
from Blueprints.CraftPackageObject import CraftPackageObject


class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets["master"] = "https://invent.kde.org/libraries/kunifiedpush"
        self.displayName = "KUnifiedPush"
        self.description = "UnifiedPush client components"
        self.defaultTarget = "master"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/qt/qtbase"] = None
        self.runtimeDependencies["libs/qt/qtwebsockets"] = None
        self.runtimeDependencies["kde/frameworks/extra-cmake-modules"] = None


class Package(CraftPackageObject.get("kde").pattern):
    def __init__(self):
        super().__init__()
