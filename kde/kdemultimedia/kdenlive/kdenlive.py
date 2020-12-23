import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()
        self.description = "Libre Video Editor, by KDE community"

    def setDependencies(self):
        self.buildDependencies["kde/frameworks/extra-cmake-modules"] = None
        self.runtimeDependencies["libs/rttr"] = None
        self.runtimeDependencies["libs/qt5/qtbase"] = None
        self.runtimeDependencies["libs/qt5/qtmultimedia"] = None
        self.runtimeDependencies["libs/qt5/qtdeclarative"] = None
        self.runtimeDependencies["libs/qt5/qtquickcontrols"] = None
        self.runtimeDependencies["libs/qt5/qtquickcontrols2"] = None
        self.runtimeDependencies["kde/frameworks/tier1/breeze-icons"] = None
        self.runtimeDependencies["kde/frameworks/tier1/karchive"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kconfig"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kcoreaddons"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kdbusaddons"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kguiaddons"] = None
        self.runtimeDependencies["kde/frameworks/tier1/ki18n"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kitemviews"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kplotting"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kwidgetsaddons"] = None
        self.runtimeDependencies["kde/frameworks/tier2/kcompletion"] = None
        self.runtimeDependencies["kde/frameworks/tier2/kcrash"] = None
        self.runtimeDependencies["kde/frameworks/tier2/kjobwidgets"] = None
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
        self.runtimeDependencies["kde/frameworks/tier3/kinit"] = None
        self.runtimeDependencies["kde/frameworks/tier3/purpose"] = None
        self.runtimeDependencies["libs/ffmpeg"] = None
        self.runtimeDependencies["libs/mlt"] = None
        self.runtimeDependencies["libs/frei0r-bigsh0t"] = None
        self.runtimeDependencies["kde/plasma/breeze"] = None
        # if CraftCore.compiler.isWindows:
        #     self.runtimeDependencies["libs/drmingw"] = None
        if CraftCore.compiler.isUnix:
            self.runtimeDependencies["kde/plasma/drkonqi"] = None


from Package.CMakePackageBase import *
from Utils import GetFiles

class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)

    def createPackage(self):
        self.whitelist_file.append(os.path.join(self.packageDir(), 'include.list'))
        self.blacklist_file.append(os.path.join(self.packageDir(), 'exclude.list'))
        self.ignoredPackages.append("libs/llvm-meta")
        self.ignoredPackages.append("data/hunspell-dictionaries")
        self.ignoredPackages.append("binary/mysql")

        self.defines["appname"] = "kdenlive"
        self.defines["icon"] = os.path.join(self.sourceDir(), "data", "icons", "kdenlive.ico")
        self.defines["icon_png"] = os.path.join(self.sourceDir(), "data", "icons", "128-apps-kdenlive.png")
        self.defines["shortcuts"] = [{"name" : "Kdenlive", "target":"bin/kdenlive.exe", "description" : self.subinfo.description}]
        self.defines["mimetypes"] = ["application/x-kdenlive"]
        self.defines["file_types"] = [".kdenlive"]
        self.defines["runenv"] = [
                'KDE_FORK_SLAVES=1',
                'MLT_REPOSITORY=$DIR/lib/mlt/',
                'MLT_DATA=$DIR/share/mlt/',
                'MLT_ROOT_DIR=$DIR/',
                'LADSPA_PATH=$DIR/lib/ladspa',
                'FREI0R_PATH=$DIR/lib/frei0r-1',
                'MLT_PROFILES_PATH=$DIR/share/mlt/profiles/',
                'MLT_PRESETS_PATH=$DIR/share/mlt/presets/',
                'SDL_AUDIODRIVER=pulseaudio']
        return TypePackager.createPackage(self)

    def postInstall(self):
        if CraftCore.compiler.isWindows:
            self.schemeDir = os.path.join(self.installDir(), 'bin', 'data', 'color-schemes')
        else:
            self.schemeDir = os.path.join(self.installDir(), 'share', 'color-schemes')
        for scheme in ['Breeze', 'BreezeDark', 'BreezeHighContrast', 'BreezeLight']:
            GetFiles.getFile('https://invent.kde.org/plasma/breeze/-/raw/master/colors/'+scheme+'.colors', self.schemeDir)
        for scheme in ['RustedBronze']:
            GetFiles.getFile('https://raw.githubusercontent.com/Bartoloni/RustedBronze/master/'+scheme+'.colors', self.schemeDir)
        return True

