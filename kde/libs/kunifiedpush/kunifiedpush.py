import info
from Blueprints.CraftPackageObject import CraftPackageObject
from CraftCore import CraftCore


class subinfo(info.infoclass):
    def setTargets(self):
        self.displayName = "KUnifiedPush"
        self.description = "UnifiedPush client components"
        self.versionInfo.setDefaultValues(gitUrl="https://invent.kde.org/libraries/kunifiedpush.git")

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/qt/qtbase"] = None
        self.runtimeDependencies["libs/qt/qtwebsockets"] = None
        self.runtimeDependencies["kde/frameworks/extra-cmake-modules"] = None
        if not CraftCore.compiler.isAndroid:
            self.runtimeDependencies["kde/frameworks/tier3/kcmutils"] = None
            self.runtimeDependencies["kde/frameworks/tier3/kservice"] = None


class Package(CraftPackageObject.get("kde").pattern):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
