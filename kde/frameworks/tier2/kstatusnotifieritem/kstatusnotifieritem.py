import info
from Blueprints.CraftPackageObject import CraftPackageObject
from CraftCore import CraftCore


class subinfo(info.infoclass):
    def registerOptions(self):
        if not CraftPackageObject.get("libs/qt").instance.subinfo.options.dynamic.qtMajorVersion == "6":
            CraftCore.log.warning("StatusNotifierItem was added in KF6, hence it is not available for lower Qt versions")
            self.parent.package.categoryInfo.compiler = CraftCore.compiler.Compiler.NoCompiler
        else:
            self.parent.package.categoryInfo.platforms &= CraftCore.compiler.Platforms.NotAndroid

        # https://invent.kde.org/frameworks/kstatusnotifieritem/-/merge_requests/6
        self.patchToApply["5.245.0"] = [("mr-6.patch", 1)]

    def setTargets(self):
        self.versionInfo.setDefaultValues()

        self.description = "KStatusNotifierItem"

    def setDependencies(self):
        self.buildDependencies["virtual/base"] = None
        self.buildDependencies["kde/frameworks/extra-cmake-modules"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kwindowsystem"] = None
        self.runtimeDependencies["libs/qt/qtbase"] = None


class Package(CraftPackageObject.get("kde/frameworks").pattern):
    def __init__(self):
        super().__init__()
