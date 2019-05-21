import info


class subinfo(info.infoclass):
    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.buildDependencies["kde/frameworks/extra-cmake-modules"] = None
        self.runtimeDependencies["libs/qt5/qtbase"] = None
        # qtquick1 is optional
        # self.runtimeDependencies["libs/qtquick1"] = None

    def setTargets(self):
        self.svnTargets["master"] = "git://anongit.kde.org/phonon"
        for ver in ["4.10.1"]:
            self.targets[ver] = f"https://download.kde.org/stable/phonon/{ver}/phonon-{ver}.tar.xz"
            self.targetDigestUrls[ver] = f"https://download.kde.org/stable/phonon/{ver}/phonon-{ver}.tar.xz.sha256"
            self.targetInstSrc[ver] = f"phonon-{ver}"
        self.description = "a Qt based multimedia framework"
        self.defaultTarget = "4.10.1"

        self.patchToApply["4.10.1"] = [
            ("phonon-4.10.1-macos-rpath.diff", 1), # fix rpath lokup issue during build
        ]
        self.patchLevel["4.10.1"] = 1


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
        self.subinfo.options.configure.args = " -DPHONON_INSTALL_QT_EXTENSIONS_INTO_SYSTEM_QT=ON -DPHONON_BUILD_PHONON4QT5=ON"
        if not self.subinfo.options.isActive("libs/dbus"):
            self.subinfo.options.configure.args += " -DPHONON_NO_DBUS=ON "

    def postInstall(self):
        brokenFiles = [ os.path.join(self.installDir(), "lib", "cmake", "phonon4qt5", "Phonon4Qt5Config.cmake"),
                        os.path.join(self.installDir(), "mkspecs", "modules", "qt_phonon4qt5.pri") ]
        return self.patchInstallPrefix(brokenFiles, OsUtils.toUnixPath(self.subinfo.buildPrefix), OsUtils.toUnixPath(CraftCore.standardDirs.craftRoot()))
