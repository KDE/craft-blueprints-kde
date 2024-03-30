import info
from Blueprints.CraftPackageObject import CraftPackageObject
from CraftCore import CraftCore
from CraftOS.osutils import OsUtils
from Package.CMakePackageBase import CMakePackageBase


class subinfo(info.infoclass):
    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.buildDependencies["kde/frameworks/extra-cmake-modules"] = None
        self.runtimeDependencies["libs/qt/qtbase"] = None
        self.buildDependencies["libs/qt6/qt5compat"] = None

    def setTargets(self):
        self.svnTargets["master"] = "https://invent.kde.org/libraries/phonon.git"
        for ver in ["4.12.0"]:
            self.targets[ver] = f"https://download.kde.org/stable/phonon/{ver}/phonon-{ver}.tar.xz"
            self.targetDigestUrls[ver] = f"https://download.kde.org/stable/phonon/{ver}/phonon-{ver}.tar.xz.sha256"
            self.targetInstSrc[ver] = f"phonon-{ver}"
        self.description = "a Qt based multimedia framework"
        self.defaultTarget = "4.12.0"


class Package(CMakePackageBase):
    def __init__(self):
        super().__init__()
        self.subinfo.options.configure.args = ["-DPHONON_INSTALL_QT_EXTENSIONS_INTO_SYSTEM_QT=ON"]
        if not self.subinfo.options.isActive("libs/dbus"):
            self.subinfo.options.configure.args += ["-DPHONON_NO_DBUS=ON"]
        self.subinfo.options.configure.args += ["-DQT_MAJOR_VERSION=6", "-DPHONON_BUILD_QT6=ON", "-DPHONON_BUILD_QT5=OFF"]

    def postInstall(self):
        libDir = self.installDir() / "lib"
        if not libDir.is_dir():
            libDir = self.installDir() / "lib64"
        if (libDir / "x86_64-linux-gnu").is_dir():
            libDir = libDir / "x86_64-linux-gnu"
        qtMajor = "6"
        brokenFiles = [libDir / f"cmake/phonon4qt{qtMajor}/Phonon4Qt{qtMajor}Config.cmake"]
        return self.patchInstallPrefix(brokenFiles, OsUtils.toUnixPath(self.subinfo.buildPrefix), OsUtils.toUnixPath(CraftCore.standardDirs.craftRoot()))
