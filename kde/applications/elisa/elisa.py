import info
from Blueprints.CraftPackageObject import CraftPackageObject
from CraftCore import CraftCore


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()

        self.displayName = "Elisa"
        self.description = "the Elisa music player"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.buildDependencies["kde/frameworks/extra-cmake-modules"] = None
        self.runtimeDependencies["libs/qt/qtbase"] = None
        self.runtimeDependencies["libs/qt/qtmultimedia"] = None
        self.runtimeDependencies["libs/qt6/qt5compat"] = None
        self.runtimeDependencies["kde/unreleased/kirigami-addons"] = None
        self.runtimeDependencies["libs/qt/qtsvg"] = None

        if CraftCore.compiler.platform.isWindows:
            self.runtimeDependencies["binary/vlc"] = None

        if not CraftCore.compiler.platform.isAndroid:
            self.runtimeDependencies["kde/frameworks/tier3/qqc2-desktop-style"] = None
            self.runtimeDependencies["kde/frameworks/tier2/kfilemetadata"] = None
            self.runtimeDependencies["kde/frameworks/tier2/kdoctools"] = None
            self.runtimeDependencies["kde/frameworks/tier2/kcrash"] = None
        else:
            self.runtimeDependencies["kde/plasma/qqc2-breeze-style"] = None

        self.runtimeDependencies["kde/frameworks/tier1/kconfig"] = None
        self.runtimeDependencies["kde/frameworks/tier1/ki18n"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kcoreaddons"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kxmlgui"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kirigami"] = None


class Package(CraftPackageObject.get("kde").pattern):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def createPackage(self):
        self.defines["executable"] = "bin\\elisa.exe"

        self.defines["icon"] = self.blueprintDir() / "elisa.ico"
        self.defines["icon_png"] = self.sourceDir() / "icons/44-apps-elisa.png"
        self.defines["icon_png_44"] = self.sourceDir() / "icons/44-apps-elisa.png"

        self.defines["mimetypes"] = ["audio/mpeg", "audio/mp4"]
        self.defines["file_types"] = [".mp3", ".ogg", ".m4a", ".flac", ".wav", ".m3u", ".opus"]

        self.blacklist_file.append(self.blueprintDir() / "blacklist.txt")

        self.ignoredPackages.append("binary/mysql")
        self.ignoredPackages.append("libs/dbus")

        return super().createPackage()
