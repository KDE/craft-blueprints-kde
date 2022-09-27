import info
from CraftConfig import *
from CraftOS.osutils import OsUtils

class subinfo( info.infoclass ):
    def setTargets( self ):
        self.displayName = "Haruna"
        self.description = "Haruna video player"
        self.svnTargets["master"] = "https://invent.kde.org/multimedia/haruna.git"
        self.defaultTarget = "0.9.1"

        for ver in ["0.9.1", "0.8.0"]:
            self.targets[ver] = f"https://invent.kde.org/multimedia/haruna/-/archive/v{ver}/haruna-v{ver}.tar.gz"
            self.targetInstSrc[ver] = f"haruna-v{ver}"
            self.archiveNames[ver] = f"haruna-v{ver}.tar.gz"

        self.targetDigests["0.9.1"] = (["d83dc77713984294e6e81068913a3a64d6477a5787cceb96430632034b8a6bf7"], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests["0.8.0"] = (["7af284278a482758c55a85c38eda386f8ea1a16d383e36ce03f9b02e76ebf44d"], CraftHash.HashAlgorithm.SHA256)

    def setDependencies( self ):
        self.buildDependencies["kde/frameworks/extra-cmake-modules"] = None
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/qt5/qtbase"] = None
        self.runtimeDependencies["libs/ffmpeg"] = None
        self.runtimeDependencies["libs/dbus"] = None
        self.runtimeDependencies["libs/mpv"] = None
        self.runtimeDependencies["libs/qt5/qtgraphicaleffects"] = None
        self.runtimeDependencies["libs/qt5/qtquickcontrols2"] = None
        self.runtimeDependencies["kde/plasma/breeze"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kconfig"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kirigami"] = None
        self.runtimeDependencies["kde/frameworks/tier1/ki18n"] = None
        self.runtimeDependencies["kde/frameworks/tier1/kcoreaddons"] = None
        self.runtimeDependencies["kde/frameworks/tier2/kdoctools"] = None
        self.runtimeDependencies["kde/frameworks/tier2/kfilemetadata"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kio"] = None
        self.runtimeDependencies["kde/frameworks/tier3/qqc2-desktop-style"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kiconthemes"] = None
        self.runtimeDependencies["kde/frameworks/tier3/kxmlgui"] = None

from Package.CMakePackageBase import *

class Package( CMakePackageBase ):
    def __init__(self):
        CMakePackageBase.__init__(self)

    def createPackage(self):
        self.defines["executable"] = "bin\\haruna.exe"

        self.defines["icon"] = os.path.join(self.packageDir(), "haruna.ico")

        self.defines["mimetypes"] = ["video/mkv", "video/mp4", "video/ogm", "video/avi"]
        self.defines["file_types"] = [".mkv", ".mp4", ".ogm", ".avi"]

        self.ignoredPackages.append("binary/mysql")
        self.ignoredPackages.append("libs/dbus")

        return TypePackager.createPackage(self)
