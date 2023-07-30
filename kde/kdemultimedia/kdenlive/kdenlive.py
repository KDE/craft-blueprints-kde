import os

import info
from CraftCore import CraftCore
from CraftOS.osutils import OsUtils


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()
        self.description = "Libre Video Editor, by KDE community"
        self.patchToApply["23.04.1"] = [("fix-sequence-length.patch", 1)]
        self.patchToApply["23.04.1"] += [("fix-help.patch", 1)]

    def setDependencies(self):
        self.buildDependencies["kde/frameworks/extra-cmake-modules"] = None
        self.runtimeDependencies["libs/qt/qtbase"] = None
        self.runtimeDependencies["libs/qt/qtmultimedia"] = None
        self.runtimeDependencies["libs/qt/qtspeech"] = None
        self.runtimeDependencies["libs/qt/qtimageformats"] = None
        self.runtimeDependencies["libs/qt/qtdeclarative"] = None
        self.runtimeDependencies["libs/qt/qtnetworkauth"] = None
        if CraftPackageObject.get("libs/qt").instance.subinfo.options.dynamic.qtMajorVersion == "5":
            self.runtimeDependencies["libs/qt5/qtquickcontrols"] = None
            self.runtimeDependencies["libs/qt5/qtquickcontrols2"] = None
        self.runtimeDependencies["kde/frameworks/tier1/breeze-icons"] = None
        self.runtimeDependencies["kde/frameworks/tier1/karchive"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kconfig"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kcoreaddons"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kguiaddons"] = None
        self.runtimeDependencies["kde/frameworks/tier1/ki18n"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kitemviews"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kplotting"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kwidgetsaddons"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kimageformats"] = None
        self.runtimeDependencies["kde/frameworks/tier2/kcompletion"] = None
        self.runtimeDependencies["kde/frameworks/tier2/kcrash"] = None
        self.runtimeDependencies["kde/frameworks/tier2/kjobwidgets"] = None
        self.runtimeDependencies["kde/frameworks/tier2/kfilemetadata"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kdeclarative"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kbookmarks"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kconfigwidgets"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kiconthemes"] = None
        if not CraftCore.compiler.isWindows:
            self.runtimeDependencies["kde/kdenetwork/kio-extras"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kio"] = None
        self.runtimeDependencies["kde/frameworks/tier3/knewstuff"] = None
        self.runtimeDependencies["kde/frameworks/tier3/knotifications"] = None
        self.runtimeDependencies["kde/frameworks/tier3/knotifyconfig"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kservice"] = None
        self.runtimeDependencies["kde/frameworks/tier3/ktextwidgets"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kxmlgui"] = None
        self.runtimeDependencies["kde/frameworks/tier3/purpose"] = None
        self.runtimeDependencies["libs/ffmpeg"] = None
        self.runtimeDependencies["libs/mlt"] = None
        self.runtimeDependencies["kde/plasma/breeze"] = None
        if not CraftCore.compiler.isMacOS:
            self.runtimeDependencies["libs/frei0r-bigsh0t"] = None
        if CraftCore.compiler.isWindows:
            self.runtimeDependencies["libs/drmingw"] = None
        if CraftCore.compiler.isLinux:
            self.runtimeDependencies["kde/plasma/drkonqi"] = None


from Blueprints.CraftPackageObject import CraftPackageObject
from Packager.AppImagePackager import AppImagePackager
from Utils import GetFiles


class Package(CraftPackageObject.get("kde").pattern):
    def __init__(self):
        CraftPackageObject.get("kde").pattern.__init__(self)
        self.subinfo.options.configure.args += ["-DNODBUS=ON"]
        if self.buildTarget == "master":
            self.subinfo.options.configure.args += ["-DRELEASE_BUILD=OFF"]

        if CraftPackageObject.get("libs/qt").instance.subinfo.options.dynamic.qtMajorVersion == "6":
            self.subinfo.options.configure.args += ["-DKF_MAJOR=6"]

    def setDefaults(self, defines: {str: str}) -> {str: str}:
        defines = super().setDefaults(defines)
        if OsUtils.isLinux() and isinstance(self, AppImagePackager):
            defines["runenv"] += [
                "PACKAGE_TYPE=appimage",
                "LD_LIBRARY_PATH=$this_dir/usr/lib/:$LD_LIBRARY_PATH",
                "MLT_REPOSITORY=$this_dir/usr/lib/mlt-7/",
                "MLT_DATA=$this_dir/usr/share/mlt-7/",
                "MLT_ROOT_DIR=$this_dir/usr/",
                "LADSPA_PATH=$this_dir/usr/lib/ladspa",
                "FREI0R_PATH=$this_dir/usr/lib/frei0r-1",
                "MLT_PROFILES_PATH=$this_dir/usr/share/mlt-7/profiles/",
                "MLT_PRESETS_PATH=$this_dir/usr/share/mlt-7/presets/",
                "QT_QPA_PLATFORM=xcb",
                "SDL_AUDIODRIVER=pulseaudio",
            ]
        return defines

    def createPackage(self):
        if not CraftCore.compiler.isMacOS:
            self.blacklist_file.append(os.path.join(self.packageDir(), "exclude.list"))
        self.addExecutableFilter(r"bin/(?!(ff|kdenlive|kioslave|melt|update-mime-database|drmingw|data/kdenlive)).*")
        self.ignoredPackages.append("libs/llvm")
        self.ignoredPackages.append("data/hunspell-dictionaries")
        self.ignoredPackages.append("binary/mysql")

        self.defines["appname"] = "kdenlive"
        self.defines["icon"] = os.path.join(self.sourceDir(), "data", "icons", "kdenlive.ico")
        self.defines["icon_png"] = os.path.join(self.sourceDir(), "data", "icons", "128-apps-kdenlive.png")
        self.defines["shortcuts"] = [{"name": "Kdenlive", "target": "bin/kdenlive.exe", "description": self.subinfo.description}]
        self.defines["file_types"] = [".kdenlive"]
        return super().createPackage()

    def postInstall(self):
        if CraftCore.compiler.isWindows:
            self.schemeDir = os.path.join(self.installDir(), "bin", "data", "color-schemes")
        else:
            self.schemeDir = os.path.join(self.installDir(), "share", "color-schemes")
        for scheme in ["RustedBronze"]:
            GetFiles.getFile("https://raw.githubusercontent.com/Bartoloni/RustedBronze/master/" + scheme + ".colors", self.schemeDir)
        return True
