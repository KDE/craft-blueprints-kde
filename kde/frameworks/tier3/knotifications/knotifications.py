import info
from Blueprints.CraftPackageObject import CraftPackageObject
from CraftCore import CraftCore
from CraftOS.osutils import OsUtils


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()

        self.patchLevel["master"] = 1

    def setDependencies(self):
        self.buildDependencies["virtual/base"] = None
        self.buildDependencies["kde/frameworks/extra-cmake-modules"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kconfig"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kcoreaddons"] = None
        self.runtimeDependencies["libs/libcanberra"] = None

        if not CraftCore.compiler.isAndroid:
            self.runtimeDependencies["libs/qt/qtspeech"] = None
            self.runtimeDependencies["kde/frameworks/tier1/kwindowsystem"] = None

        if OsUtils.isWin():
            self.runtimeDependencies["dev-utils/snoretoast"] = None


class Package(CraftPackageObject.get("kde/frameworks").pattern):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
