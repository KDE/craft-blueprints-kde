import info
from Blueprints.CraftPackageObject import CraftPackageObject
from CraftCore import CraftCore
from Packager.AppImagePackager import AppImagePackager
from Utils import GetFiles


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()
        self.description = "Libre Video Editor, by KDE community"

    def setDependencies(self):
        self.buildDependencies["kde/frameworks/extra-cmake-modules"] = None
        self.runtimeDependencies["libs/qt/qtbase"] = None
        self.runtimeDependencies["libs/qt/qtmultimedia"] = None
        self.runtimeDependencies["libs/qt/qtspeech"] = None
        self.runtimeDependencies["libs/qt/qtimageformats"] = None
        self.runtimeDependencies["libs/qt/qtdeclarative"] = None
        self.runtimeDependencies["libs/qt/qtnetworkauth"] = None
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
        self.runtimeDependencies["kde/frameworks/tier2/kcolorscheme"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kdeclarative"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kbookmarks"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kconfigwidgets"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kiconthemes"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kio"] = None
        self.runtimeDependencies["kde/frameworks/tier3/knewstuff"] = None
        self.runtimeDependencies["kde/frameworks/tier3/knotifications"] = None
        self.runtimeDependencies["kde/frameworks/tier3/knotifyconfig"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kservice"] = None
        self.runtimeDependencies["kde/frameworks/tier3/ktextwidgets"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kxmlgui"] = None
        self.runtimeDependencies["kde/frameworks/tier3/purpose"] = None
        self.runtimeDependencies["kde/frameworks/tier4/frameworkintegration"] = None
        self.runtimeDependencies["kde/kdenetwork/kio-extras"] = None
        self.runtimeDependencies["kde/kdemultimedia/ffmpegthumbs"] = None
        self.runtimeDependencies["libs/ffmpeg"] = None
        self.runtimeDependencies["libs/mlt"] = None
        self.runtimeDependencies["libs/opentimelineio"] = None
        self.runtimeDependencies["kde/plasma/breeze"] = None
        if not CraftCore.compiler.isMacOS:
            self.runtimeDependencies["libs/frei0r-bigsh0t"] = None
        # DrMinGW needs build fixes with MinGW 13 before we can re-enable it
        # if CraftCore.compiler.isWindows:
        #     self.runtimeDependencies["libs/drmingw"] = None
        # DrKonqi disabled for now as it needs polkit since KF6 and this requires lots of other dependencies
        # if CraftCore.compiler.isLinux:
        #    self.runtimeDependencies["kde/plasma/drkonqi"] = None
        # Appimage - warning, causes external process crashes
        # self.buildDependencies["dev-utils/linuxdeploy-plugin-checkrt"] = None


class Package(CraftPackageObject.get("kde").pattern):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subinfo.options.configure.args += ["-DUSE_DBUS=OFF", "-DFETCH_OTIO=OFF"]
        if self.buildTarget == "master":
            self.subinfo.options.configure.args += ["-DRELEASE_BUILD=OFF"]

    def setDefaults(self, defines: {str: str}) -> {str: str}:
        defines = super().setDefaults(defines)
        if CraftCore.compiler.isLinux and isinstance(self, AppImagePackager):
            defines["runenv"] += [
                "PACKAGE_TYPE=appimage",
                "MLT_REPOSITORY=$this_dir/usr/lib/mlt-7/",
                "MLT_DATA=$this_dir/usr/share/mlt-7/",
                "MLT_ROOT_DIR=$this_dir/usr/",
                "MLT_APPDIR=$this_dir/usr/",
                "LADSPA_PATH=$this_dir/usr/lib/ladspa",
                "FREI0R_PATH=$this_dir/usr/lib/frei0r-1",
                "MLT_PROFILES_PATH=$this_dir/usr/share/mlt-7/profiles/",
                "MLT_PRESETS_PATH=$this_dir/usr/share/mlt-7/presets/",
                "SDL_AUDIODRIVER=pulseaudio",
                "ALSA_CONFIG_DIR=/usr/share/alsa",
                "ALSA_PLUGIN_DIR=/usr/lib/x86_64-linux-gnu/alsa-lib",
                "LIBVA_DRIVERS_PATH=/usr/lib/dri:/usr/lib64/dri:/usr/lib/x86_64-linux-gnu/dri:/usr/lib/aarch64-linux-gnu/dri",
            ]
        return defines

    def createPackage(self):
        if not CraftCore.compiler.isMacOS:
            self.blacklist_file.append(self.blueprintDir() / "exclude.list")
        else:
            self.blacklist_file.append(self.blueprintDir() / "exclude_macos.list")
        self.addExecutableFilter(r"bin/(?!(ff|kdenlive|kioworker|melt|update-mime-database|snoretoast|drmingw|data/kdenlive)).*")
        self.ignoredPackages.append("libs/llvm")
        self.ignoredPackages.append("data/hunspell-dictionaries")
        self.ignoredPackages.append("binary/mysql")

        self.defines["appname"] = "kdenlive"
        self.defines["icon"] = self.sourceDir() / "data/icons/kdenlive.ico"
        self.defines["icon_png"] = self.sourceDir() / "data/icons/128-apps-kdenlive.png"
        self.defines["shortcuts"] = [{"name": "Kdenlive", "target": "bin/kdenlive.exe", "description": self.subinfo.description}]
        self.defines["file_types"] = [".kdenlive"]
        # Appimage
        # self.defines["appimage_extra_plugins"] = ["checkrt"]
        return super().createPackage()

    def postInstall(self):
        if CraftCore.compiler.isWindows:
            self.schemeDir = self.installDir() / "bin/data/color-schemes"
        else:
            self.schemeDir = self.installDir() / "share/color-schemes"
        for scheme in ["RustedBronze"]:
            GetFiles.getFile(f"https://raw.githubusercontent.com/Bartoloni/RustedBronze/master/{scheme}.colors", self.schemeDir)
        return True
