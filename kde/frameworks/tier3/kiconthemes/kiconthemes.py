import info
from Blueprints.CraftPackageObject import CraftPackageObject
from Blueprints.CraftVersion import CraftVersion
from CraftCore import CraftCore


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()

        self.patchToApply["6.4.0"] = [("libpath.diff", 1)]
        self.patchLevel["6.4.0"] = 5

        # Android icon recoloring
        # See https://invent.kde.org/frameworks/kiconthemes/-/merge_requests/154
        self.patchToApply["6.5.0"] = ("154.patch", 1)
        self.patchLevel["6.5.0"] = 1

        self.description = "Classes to improve the handling of icons"

    def setDependencies(self):
        self.buildDependencies["virtual/base"] = None
        self.buildDependencies["kde/frameworks/extra-cmake-modules"] = None
        self.runtimeDependencies["libs/qt/qtbase"] = None
        self.runtimeDependencies["libs/qt/qtsvg"] = None
        self.runtimeDependencies["kde/frameworks/tier1/karchive"] = None
        self.runtimeDependencies["kde/frameworks/tier1/ki18n"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kwidgetsaddons"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kitemviews"] = None
        self.runtimeDependencies["kde/frameworks/tier2/kcolorscheme"] = None
        if self.buildTarget < CraftVersion("6.8.0"):
            self.runtimeDependencies["kde/frameworks/tier3/kconfigwidgets"] = None

        if not CraftCore.compiler.platform.isAndroid:
            self.runtimeDependencies["kde/frameworks/tier1/breeze-icons"] = None


class Package(CraftPackageObject.get("kde/frameworks").pattern):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
