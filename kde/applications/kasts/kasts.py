import info
from Blueprints.CraftPackageObject import CraftPackageObject
from CraftCore import CraftCore


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues(gitUrl="https://invent.kde.org/multimedia/kasts.git")
        self.displayName = "Kasts"
        self.description = "Podcast player"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/qt/qtbase"] = None
        self.runtimeDependencies["libs/qt/qtdeclarative"] = None
        self.runtimeDependencies["libs/qt/qtsvg"] = None
        if not CraftCore.compiler.compiler.isMSVC:  # no mpv on MSVC
            self.runtimeDependencies["kde/unreleased/mpvqt"] = None
        self.runtimeDependencies["libs/qt/qtmultimedia"] = None
        self.runtimeDependencies["libs/taglib"] = None
        self.runtimeDependencies["qt-libs/qtkeychain"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kirigami"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kcoreaddons"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kconfig"] = None
        self.runtimeDependencies["kde/frameworks/tier1/ki18n"] = None
        self.runtimeDependencies["kde/frameworks/tier2/syndication"] = None
        self.runtimeDependencies["kde/frameworks/tier1/threadweaver"] = None
        self.runtimeDependencies["kde/unreleased/kirigami-addons"] = None
        if not CraftCore.compiler.platform.isAndroid:
            self.runtimeDependencies["kde/frameworks/tier1/breeze-icons"] = None
            self.runtimeDependencies["kde/frameworks/tier3/qqc2-desktop-style"] = None
            self.runtimeDependencies["kde/plasma/breeze"] = None
        else:
            self.runtimeDependencies["kde/plasma/qqc2-breeze-style"] = None

        if CraftCore.compiler.platform.isWindows:
            self.runtimeDependencies["binary/vlc"] = None


class Package(CraftPackageObject.get("kde").pattern):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.blacklist_file.append(self.blueprintDir() / "blacklist.txt")

    def createPackage(self):
        self.defines["executable"] = r"bin\kasts.exe"
        self.addExecutableFilter(r"(bin|libexec)/(?!(kasts|update-mime-database)).*")
        self.ignoredPackages.append("binary/mysql")
        if not CraftCore.compiler.platform.isLinux:
            self.ignoredPackages.append("libs/dbus")
        return super().createPackage()
