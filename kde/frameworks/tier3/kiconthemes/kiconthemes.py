import info
from Blueprints.CraftPackageObject import CraftPackageObject
from CraftCore import CraftCore


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()

        # enforce iconengine plugin is there on mac and Windows, on Linux this kills e.g. other Qt apps
        if CraftCore.compiler.isMacOS or CraftCore.compiler.isWindows:
            for ver in ["master"] + self.versionInfo.tarballs():
                self.patchToApply[ver] = [("svgiconengine.diff", 1)]
                self.patchLevel[ver] = 1

        self.description = "Classes to improve the handling of icons"

    def setDependencies(self):
        self.buildDependencies["virtual/base"] = None
        self.buildDependencies["kde/frameworks/extra-cmake-modules"] = None
        self.runtimeDependencies["libs/qt/qtbase"] = None
        self.runtimeDependencies["libs/qt/qtsvg"] = None
        self.runtimeDependencies["kde/frameworks/tier1/karchive"] = None
        self.runtimeDependencies["kde/frameworks/tier1/ki18n"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kconfigwidgets"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kwidgetsaddons"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kitemviews"] = None

        if not CraftCore.compiler.isAndroid:
            self.runtimeDependencies["kde/frameworks/tier1/breeze-icons"] = None


class Package(CraftPackageObject.get("kde/frameworks").pattern):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
