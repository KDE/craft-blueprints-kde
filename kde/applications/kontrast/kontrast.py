import info
from Blueprints.CraftPackageObject import CraftPackageObject
from CraftCore import CraftCore


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues(gitUrl="https://invent.kde.org/accessibility/kontrast")
        self.description = "Tool to check contrast for colors that allows verifying that your colors are correctly accessible"

    def setDependencies(self):
        self.buildDependencies["virtual/base"] = None
        self.buildDependencies["kde/frameworks/extra-cmake-modules"] = None
        self.runtimeDependencies["libs/qt/qtbase"] = None
        self.runtimeDependencies["libs/qt/qtdeclarative"] = None
        self.runtimeDependencies["kde/frameworks/tier1/ki18n"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kirigami"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kcoreaddons"] = None
        self.runtimeDependencies["kde/libs/futuresql"] = None
        self.runtimeDependencies["kde/unreleased/kirigami-addons"] = None
        if not CraftCore.compiler.isAndroid:
            self.runtimeDependencies["kde/frameworks/tier1/breeze-icons"] = None
            self.runtimeDependencies["kde/frameworks/tier3/qqc2-desktop-style"] = None
            self.runtimeDependencies["kde/plasma/breeze"] = None
        else:
            self.runtimeDependencies["kde/plasma/qqc2-breeze-style"] = None
        self.runtimeDependencies["qt-libs/qcoro"] = None


class Package(CraftPackageObject.get("kde").pattern):
    def __init__(self):
        super().__init__()
        self.blacklist_file.append(self.blueprintDir() / "blacklist.txt")
        self.defines["executable"] = r"bin\kontrast.exe"
        self.addExecutableFilter(r"(bin|libexec)/(?!(kontrast|update-mime-database)).*")
        self.ignoredPackages.append("binary/mysql")
        self.ignoredPackages.append("libs/dbus")
