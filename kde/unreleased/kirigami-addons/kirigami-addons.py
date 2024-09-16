import info
from Blueprints.CraftPackageObject import CraftPackageObject
from CraftCore import CraftCore


class subinfo(info.infoclass):
    def setTargets(self):
        self.description = "Addons for the Kirigami Framework"

        self.svnTargets["master"] = "https://invent.kde.org/libraries/kirigami-addons.git"

        # stable
        for ver in ["1.5.0", "1.6.0"]:
            self.targets[ver] = f"https://download.kde.org/stable/kirigami-addons/kirigami-addons-{ver}.tar.xz"
            self.targetDigestUrls[ver] = f"https://download.kde.org/stable/kirigami-addons/kirigami-addons-{ver}.tar.xz.sha256"
            self.targetInstSrc[ver] = "kirigami-addons-" + ver

        # Fix Android with Qt 6.8
        # See https://invent.kde.org/libraries/kirigami-addons/-/merge_requests/282
        # and https://invent.kde.org/libraries/kirigami-addons/-/merge_requests/287
        # and https://invent.kde.org/libraries/kirigami-addons/-/commit/de9ac417150a8753971124a76be727284584f308
        # and https://invent.kde.org/libraries/kirigami-addons/-/merge_requests/291
        self.patchToApply["1.5.0"] = [
            ("282.patch", 1),
            ("add-missing-coreaddons-dependency.diff", 1),
            ("de9ac417150a8753971124a76be727284584f308.patch", 1),
            ("fix-android-native-date-time-picker.diff", 1),
        ]
        self.patchLevel["1.5.0"] = 3

        self.defaultTarget = "1.6.0"

    def setDependencies(self):
        self.buildDependencies["virtual/base"] = None
        self.buildDependencies["kde/frameworks/extra-cmake-modules"] = None
        self.runtimeDependencies["libs/qt/qtbase"] = None
        self.runtimeDependencies["libs/qt/qtdeclarative"] = None
        self.runtimeDependencies["libs/qt/qtmultimedia"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kconfig"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kcoreaddons"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kguiaddons"] = None
        self.runtimeDependencies["kde/frameworks/tier1/ki18n"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kirigami"] = None
        if CraftCore.compiler.isLinux or CraftCore.compiler.isFreeBSD:
            self.runtimeDependencies["kde/frameworks/tier3/kglobalaccel"] = None


class Package(CraftPackageObject.get("kde").pattern):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
