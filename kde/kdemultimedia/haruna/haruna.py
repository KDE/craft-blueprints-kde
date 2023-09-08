import info
from CraftConfig import *
from CraftOS.osutils import OsUtils


class subinfo(info.infoclass):
    def setTargets(self):
        self.displayName = "Haruna"
        self.description = "Haruna video player"
        self.svnTargets["master"] = "https://invent.kde.org/multimedia/haruna.git"
        self.defaultTarget = "0.12.1"

        for ver in ["0.12.1","0.11.3", "0.10.3", "0.9.3"]:
            self.targets[ver] = f"https://download.kde.org/stable/haruna/haruna-{ver}.tar.xz"
            self.targetInstSrc[ver] = f"haruna-{ver}"
            self.archiveNames[ver] = f"haruna-{ver}.tar.gz"

        self.targetDigests["0.12.1"] = (["0435b336d9a19097920f1d92fe5df2e352a9431bd84ce6a34fe225930ea38ede"], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests["0.11.3"] = (["f7a2823601e0e76f7eb65d0b41eb644f5ae6ab8037d309b253d8b9baebba6f75"], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests["0.10.3"] = (["4d21eaa709dd3b9f393e2252c4642127ab5da9781a74c903dafba64ae3f9d296"], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests["0.9.3"] = (["673d8db5d59e1c0f5937c3b73c11ee858fbd43d65efcde91aba9dcf70dac73e6"], CraftHash.HashAlgorithm.SHA256)

        if OsUtils.isWin():
            self.patchToApply["0.12.1"] = [("0001-fix-Windows-build.patch", 1)]
            self.patchLevel["0.12.1"] = 1

    def setDependencies(self):
        self.buildDependencies["kde/frameworks/extra-cmake-modules"] = None
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/qt/qtbase"] = None
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


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
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
