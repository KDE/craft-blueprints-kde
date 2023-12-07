import info
from CraftConfig import *
from CraftOS.osutils import OsUtils


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()

        self.displayName = "Elisa"
        self.description = "the Elisa music player"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.buildDependencies["kde/frameworks/extra-cmake-modules"] = None
        self.runtimeDependencies["libs/qt/qtbase"] = None
        self.runtimeDependencies["libs/qt5/qtgraphicaleffects"] = None
        self.runtimeDependencies["libs/qt/qtmultimedia"] = None
        self.runtimeDependencies["libs/qt5/qtquickcontrols"] = None
        if CraftPackageObject.get("libs/qt").instance.subinfo.options.dynamic.qtMajorVersion == "5":
            self.runtimeDependencies["libs/qt5/qtquickcontrols2"] = None
        self.runtimeDependencies["libs/qt/qtsvg"] = None
        if CraftCore.compiler.isAndroid:
            if CraftPackageObject.get("libs/qt").instance.subinfo.options.dynamic.qtMajorVersion == "5":
                self.runtimeDependencies["libs/qt5/qtandroidextras"] = None
            self.runtimeDependencies["kde/plasma/qqc2-breeze-style"] = None

        if CraftCore.compiler.isWindows:
            self.runtimeDependencies["libs/qt5/qtwinextras"] = None
            self.runtimeDependencies["binary/vlc"] = None

        if not CraftCore.compiler.isAndroid:
            self.runtimeDependencies["kde/frameworks/tier3/qqc2-desktop-style"] = None
            self.runtimeDependencies["kde/frameworks/tier2/kfilemetadata"] = None
            self.runtimeDependencies["kde/frameworks/tier3/kdeclarative"] = None
            self.runtimeDependencies["kde/frameworks/tier2/kdoctools"] = None
            self.runtimeDependencies["kde/frameworks/tier2/kcrash"] = None

        self.runtimeDependencies["kde/frameworks/tier1/kconfig"] = None
        self.runtimeDependencies["kde/frameworks/tier1/ki18n"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kcoreaddons"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kxmlgui"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kirigami"] = None


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)

    def createPackage(self):
        self.defines["executable"] = "bin\\elisa.exe"

        self.defines["icon"] = os.path.join(self.packageDir(), "elisa.ico")
        self.defines["icon_png"] = os.path.join(self.sourceDir(), "icons", "44-apps-elisa.png")
        self.defines["icon_png_44"] = os.path.join(self.sourceDir(), "icons", "44-apps-elisa.png")

        self.defines["mimetypes"] = ["audio/mpeg", "audio/mp4"]
        self.defines["file_types"] = [".mp3", ".ogg", ".m4a", ".flac", ".wav", ".m3u", ".opus"]

        self.blacklist_file.append(os.path.join(self.packageDir(), "blacklist.txt"))

        self.ignoredPackages.append("binary/mysql")
        self.ignoredPackages.append("libs/dbus")

        return super().createPackage()
