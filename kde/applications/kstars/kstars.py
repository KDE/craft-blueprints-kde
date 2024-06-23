import os

import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()

        self.description = "a desktop planetarium"
        self.svnTargets["3.6.9"] = "https://invent.kde.org/education/kstars.git|stable-3.6.9"
        self.svnTargets["3.7.0"] = "https://invent.kde.org/education/kstars.git|stable-3.7.0"
        self.svnTargets["3.7.1"] = "https://invent.kde.org/education/kstars.git|stable-3.7.1"
        self.patchToApply["3.7.1"] = [("kstars-3.7.1-20240620.diff", 1)]
        self.svnTargets["master"] = "https://github.com/KDE/kstars.git"
        self.defaultTarget = "3.7.1"
        self.displayName = "KStars Desktop Planetarium"

    def setDependencies(self):
        self.runtimeDependencies["libs/qt/qtbase"] = None
        self.runtimeDependencies["libs/qt/qtdeclarative"] = None
        self.runtimeDependencies["libs/qt5/qtquickcontrols"] = None
        self.runtimeDependencies["libs/qt5/qtquickcontrols2"] = None
        self.runtimeDependencies["libs/qt/qtsvg"] = None
        self.runtimeDependencies["libs/qt5/qtdatavis3d"] = None
        self.runtimeDependencies["libs/qt/qtwebsockets"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kconfig"] = None
        self.runtimeDependencies["kde/frameworks/tier2/kdoctools"] = None
        self.runtimeDependencies["kde/frameworks/tier2/kpackage"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kwidgetsaddons"] = None
        self.runtimeDependencies["kde/frameworks/tier3/knewstuff"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kdbusaddons"] = None
        self.runtimeDependencies["kde/frameworks/tier1/ki18n"] = None
        self.runtimeDependencies["kde/frameworks/tier2/kjobwidgets"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kio"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kxmlgui"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kplotting"] = None
        self.runtimeDependencies["kde/frameworks/tier3/knotifications"] = None
        self.runtimeDependencies["kde/frameworks/tier3/knotifyconfig"] = None
        self.runtimeDependencies["libs/eigen3"] = None
        self.runtimeDependencies["libs/cfitsio"] = None
        self.runtimeDependencies["libs/libxisf"] = None
        self.runtimeDependencies["libs/wcslib"] = None
        self.runtimeDependencies["libs/libraw"] = None
        self.runtimeDependencies["libs/gsl"] = None
        self.runtimeDependencies["libs/zlib"] = None
        self.runtimeDependencies["libs/stellarsolver"] = None
        self.runtimeDependencies["qt-libs/qtkeychain"] = None

        # MacOS and Linux build indi client/server, Windows builds indi client only
        self.runtimeDependencies["libs/indilib/indi"] = None
        self.runtimeDependencies["libs/indilib/indi-3rdparty"] = None

        if CraftCore.compiler.isMacOS or CraftCore.compiler.isLinux:
            self.runtimeDependencies["libs/xplanet"] = None
            self.runtimeDependencies["libs/gsc"] = None

        if CraftCore.compiler.isLinux:
            self.buildDependencies["libs/libftdi"] = None
            self.runtimeDependencies["qt-libs/phonon-vlc"] = None
            self.runtimeDependencies["kde/frameworks/tier1/breeze-icons"] = None
            self.runtimeDependencies["libs/iconv"] = None
            self.runtimeDependencies["libs/libftdi"] = None

from Package.CMakePackageBase import *
from Packager.AppxPackager import AppxPackager


class Package(CMakePackageBase):
    def __init__(self):
        super().__init__()
        self.ignoredPackages.append("binary/mysql")
        self.ignoredPackages.append("libs/llvm")
        if CraftCore.compiler.isWindows:
            self.blacklist_file.append(os.path.join(self.blueprintDir(), "win-blacklist.txt"))
        if CraftCore.compiler.isMacOS:
            self.blacklist_file.append(os.path.join(self.blueprintDir(), "mac-blacklist.txt"))
        self.subinfo.options.configure.args += [
            "-DBUILD_DOC=OFF",
            "-DBUILD_TESTING=OFF"]

    def make(self):
        if not super().make():
            return False

        if CraftCore.compiler.isMacOS:

            # 	Defining Craft Directories
            buildDir = str(self.buildDir())
            sourceDir = str(self.sourceDir())
            packageDir = str(self.blueprintDir())
            imageDir = str(self.imageDir())
            craftRoot = str(CraftCore.standardDirs.craftRoot())
            craftLibDir = os.path.join(craftRoot, "lib")
            KSTARS_APP = os.path.join(buildDir, "bin", "KStars.app")
            KSTARS_RESOURCES = os.path.join(KSTARS_APP, "Contents", "Resources")
            KSTARS_PLUGINS = os.path.join(KSTARS_APP, "Contents", "Plugins")

            # KIO Slave and it's parts (For loading thumbnail images)
            utils.system("cp -rf " + craftRoot + "/lib/libexec/kf5/kioslave5 " + KSTARS_APP + "/Contents/MacOS/")
            utils.system("mkdir -p " + KSTARS_PLUGINS + "/kf5/kio")
            utils.system("cp -f " + craftRoot + "/plugins/kf5/kio/kio_file.so " + KSTARS_PLUGINS + "/kf5/kio/")
            utils.system("cp -f " + craftRoot + "/plugins/kf5/kio/kio_http.so " + KSTARS_PLUGINS + "/kf5/kio/")

            # The Translations Directory
            utils.system("cp -rf " + craftRoot + "/share/locale " + KSTARS_RESOURCES)

            for path in utils.getLibraryDeps(str(KSTARS_APP + "/Contents/MacOS/kstars")):
                if path.startswith(craftLibDir):
                    utils.system(["install_name_tool", "-change", path, os.path.join("@rpath", os.path.basename(path)), KSTARS_APP + "/Contents/MacOS/kstars"])

        return True

    def createPackage(self):
        self.defines["executable"] = "bin\\kstars.exe"
        # self.defines["setupname"] = "kstars-latest-win64.exe"
        self.defines["icon"] = os.path.join(self.blueprintDir(), "kstars.ico")
        # TODO: support dpi scaling
        # TODO: use assets from src with the next release
        # self.defines["icon_png"] = os.path.join(self.sourceDir(), "packaging", "windows", "assets", "Square150x150Logo.scale-100.png")
        # self.defines["icon_png_44"] = os.path.join(self.sourceDir(), "packaging", "windows", "assets", "Square44x44Logo.scale-100.png")
        # self.defines["icon_png_310x150"] = os.path.join(self.sourceDir(), "packaging", "windows", "assets", "Wide310x150Logo.scale-100.png")
        # self.defines["icon_png_310x310"] = os.path.join(self.sourceDir(), "packaging", "windows", "assets", "Square310x310Logo.scale-100.png")
        self.defines["icon_png"] = os.path.join(self.blueprintDir(), ".assets", "Square150x150Logo.scale-100.png")
        self.defines["icon_png_44"] = os.path.join(self.blueprintDir(), ".assets", "Square44x44Logo.scale-100.png")
        self.defines["icon_png_310x150"] = os.path.join(self.blueprintDir(), ".assets", "Wide310x150Logo.scale-100.png")
        self.defines["icon_png_310x310"] = os.path.join(self.blueprintDir(), ".assets", "Square310x310Logo.scale-100.png")
        if isinstance(self, AppxPackager):
            self.defines["display_name"] = "KStars"

        return super().createPackage()
