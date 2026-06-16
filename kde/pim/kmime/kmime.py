import info
from Blueprints.CraftPackageObject import CraftPackageObject
from Blueprints.CraftVersion import CraftVersion
from CraftCore import CraftCore


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()

        self.description = "KMime library"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.buildDependencies["kde/frameworks/extra-cmake-modules"] = None
        self.runtimeDependencies["libs/qt/qtbase"] = None
        self.runtimeDependencies["kde/frameworks/tier1/ki18n"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kcodecs"] = None

        # superseded by kde/frameworks/tier2/kmime after 26.04
        if self.buildTarget == "master" or CraftVersion(self.buildTarget) > CraftVersion("26.04.3"):
            self.parent.package.categoryInfo.platforms = CraftCore.compiler.Platforms.NoPlatform


class Package(CraftPackageObject.get("kde").pattern):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subinfo.options.configure.args += ["-DUSE_UNITY_CMAKE_SUPPORT=ON"]
