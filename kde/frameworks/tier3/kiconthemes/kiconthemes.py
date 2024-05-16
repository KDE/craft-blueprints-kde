import info
from Blueprints.CraftPackageObject import CraftPackageObject
from Blueprints.CraftVersion import CraftVersion
from CraftCore import CraftCore


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()

        self.patchToApply["6.1.0"] = [("kiconthemes-6.1.0-20240415.diff", 1)]
        # enforce iconengine plugin is there on mac and Windows, on Linux this kills e.g. other Qt apps
        for ver in self.versionInfo.tarballs():
            if ver < CraftVersion("6.2.0"):
                if CraftCore.compiler.isMacOS or CraftCore.compiler.isWindows:
                    if ver not in self.patchToApply:
                        self.patchToApply[ver] = []
                    self.patchToApply[ver] += [("svgiconengine.diff", 1)]
                    self.patchLevel[ver] = 1
                elif not CraftCore.compiler.isAndroid:
                    # required for AppImage icon coloring
                    if ver not in self.patchToApply:
                        self.patchToApply[ver] = []
                    self.patchToApply[ver] += [("registericonengine.diff", 1)]
        self.patchLevel["6.1.0"] = 3
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
        if CraftVersion("6.2.0") <= self.buildTarget <= CraftVersion("6.2.99"):
            self.subinfo.options.configure.args += ["-DKICONTHEMES_REGISTER_ICON_PLUGIN=ON"]
