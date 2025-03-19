import info
from Blueprints.CraftPackageObject import CraftPackageObject
from CraftCore import CraftCore


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()

        self.patchLevel["master"] = 1

        # Fix for Android 14 or higher, needed before KF 6.10
        # See https://invent.kde.org/frameworks/knotifications/-/merge_requests/160
        self.patchToApply["6.8.0"] = [("android-14-fix.diff", 1)]
        self.patchLevel["6.8.0"] = 1
        self.patchToApply["6.9.0"] = [("android-14-fix.diff", 1)]

    def setDependencies(self):
        self.buildDependencies["virtual/base"] = None
        self.buildDependencies["kde/frameworks/extra-cmake-modules"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kconfig"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kcoreaddons"] = None
        self.runtimeDependencies["libs/libcanberra"] = None

        if not CraftCore.compiler.isAndroid:
            self.runtimeDependencies["libs/qt/qtspeech"] = None
            self.runtimeDependencies["kde/frameworks/tier1/kwindowsystem"] = None

        if CraftCore.compiler.isWindows:
            self.runtimeDependencies["dev-utils/snoretoast"] = None


class Package(CraftPackageObject.get("kde/frameworks").pattern):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
