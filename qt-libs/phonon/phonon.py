import info


class subinfo(info.infoclass):
    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.buildDependencies["kde/frameworks/extra-cmake-modules"] = None
        self.runtimeDependencies["libs/qt/qtbase"] = None
        # qtquick1 is optional
        # self.runtimeDependencies["libs/qtquick1"] = None

    def setTargets(self):
        self.svnTargets["master"] = "https://anongit.kde.org/phonon"
        for ver in ["4.10.1", "4.11.1"]:
            self.targets[ver] = f"https://download.kde.org/stable/phonon/{ver}/phonon-{ver}.tar.xz"
            self.targetDigestUrls[ver] = f"https://download.kde.org/stable/phonon/{ver}/phonon-{ver}.tar.xz.sha256"
            self.targetInstSrc[ver] = f"phonon-{ver}"
        self.description = "a Qt based multimedia framework"
        self.defaultTarget = "4.11.1"

        self.patchToApply["4.10.1"] = [
            ("phonon-4.10.1-macos-rpath.diff", 1), # fix rpath lokup issue during build
        ]
        self.patchLevel["4.10.1"] = 1


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
        self.subinfo.options.configure.args = ["-DPHONON_INSTALL_QT_EXTENSIONS_INTO_SYSTEM_QT=ON", "-DPHONON_BUILD_PHONON4QT5=ON"]
        if not self.subinfo.options.isActive("libs/dbus"):
            self.subinfo.options.configure.args += ["-DPHONON_NO_DBUS=ON"]
        if CraftPackageObject.get("libs/qt").instance.subinfo.options.dynamic.qtMajorVersion == "6":
            self.subinfo.options.configure.args += ["-DQT_MAJOR_VERSION=6", "-DEXCLUDE_DEPRECATED_BEFORE_AND_AT=5.99.0"]

    def postInstall(self):
        libDir = self.installDir() / "lib"
        if not libDir.is_dir():
            libDir = self.installDir() / "lib64"
        if (libDir / "x86_64-linux-gnu").is_dir():
            libDir = libDir / "x86_64-linux-gnu"
        qtMajor = CraftPackageObject.get("libs/qt").instance.subinfo.options.dynamic.qtMajorVersion
        brokenFiles = [ os.path.join(libDir, "cmake", f"phonon4qt{qtMajor}", f"Phonon4Qt{qtMajor}Config.cmake"),
                        os.path.join(self.installDir(), "mkspecs", "modules", f"qt_phonon4qt{qtMajor}.pri") ]
        return self.patchInstallPrefix(brokenFiles, OsUtils.toUnixPath(self.subinfo.buildPrefix), OsUtils.toUnixPath(CraftCore.standardDirs.craftRoot()))
