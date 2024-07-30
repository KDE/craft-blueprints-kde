import info
from CraftCore import CraftCore
from Blueprints.CraftPackageObject import CraftPackageObject
from Blueprints.CraftVersion import CraftVersion


class subinfo(info.infoclass):
    def setTargets(self):
        self.description = "Addons for the Kirigami Framework"

        self.svnTargets["master"] = "https://invent.kde.org/libraries/kirigami-addons.git"

        # stable
        for ver in ["1.3.0", "1.4.0"]:
            self.targets[ver] = f"https://download.kde.org/stable/kirigami-addons/kirigami-addons-{ver}.tar.xz"
            self.targetDigestUrls[ver] = f"https://download.kde.org/stable/kirigami-addons/kirigami-addons-{ver}.tar.xz.sha256"
            self.targetInstSrc[ver] = "kirigami-addons-" + ver

        self.defaultTarget = "1.4.0"

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
