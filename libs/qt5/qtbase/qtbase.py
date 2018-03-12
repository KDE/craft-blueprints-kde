# -*- coding: utf-8 -*-

import info
from Package.Qt5CorePackageBase import *


class subinfo(info.infoclass):
    def setTargets(self):
        self.versionInfo.setDefaultValues()

        for ver in self.versionInfo.tarballs() + self.versionInfo.branches() + self.versionInfo.tags():
            qtVer = CraftVersion(ver)
            if ver == "dev":
                self.patchToApply[ver] = []
            elif qtVer >= CraftVersion("5.10"):
                self.patchToApply[ver] = [
                    ("qdbus-manager-quit-5.7.patch", 1), # https://phabricator.kde.org/D2545#69186
                    ("0001-Fix-private-headers.patch", 1),  # https://bugreports.qt.io/browse/QTBUG-37417
                    ("workaround-mingw-egl.diff", 1)
                ]
            elif qtVer >= CraftVersion("5.9.4") or qtVer == CraftVersion("5.9"):
                self.patchToApply[ver] = [
                    ("qdbus-manager-quit-5.7.patch", 1),  # https://phabricator.kde.org/D2545#69186
                    ("0001-Fix-private-headers.patch", 1),  # https://bugreports.qt.io/browse/QTBUG-37417
                    ("workaround-mingw-egl-qt5.9.4.diff", 1),
                    ("0001-Add-APPDIR-data-APPNAME-5.9.4.patch", 1),  # https://codereview.qt-project.org/#/c/197855/
                ]
            elif qtVer >= CraftVersion("5.9.3"):
                self.patchToApply[ver] = [
                    ("qdbus-manager-quit-5.7.patch", 1),  # https://phabricator.kde.org/D2545#69186
                    ("0001-Fix-private-headers.patch", 1),  # https://bugreports.qt.io/browse/QTBUG-37417
                    ("0001-Add-APPDIR-data-APPNAME-to-the-non-Generic-paths-on-.patch", 1)]  # https://codereview.qt-project.org/#/c/197855/
            elif qtVer >= CraftVersion("5.9"):
                self.patchToApply[ver] = [
                    ("fix-angle-mingw.patch", 1),
                    ("qtbase-5.8.patch", 1),  # https://codereview.qt-project.org/#/c/149550/
                    ("qdbus-manager-quit-5.7.patch", 1),  # https://phabricator.kde.org/D2545#69186
                    ("hack-fix-syncqt.patch", 1),
                    ("0001-Fix-private-headers.patch", 1),  # https://bugreports.qt.io/browse/QTBUG-37417
                    ("0001-Add-APPDIR-data-APPNAME-to-the-non-Generic-paths-on-.patch", 1)]  # https://codereview.qt-project.org/#/c/197855/
            elif qtVer >= CraftVersion("5.8"):
                self.patchToApply[ver] = [
                    ("fix-angle-mingw.patch", 1),
                    ("qtbase-5.8.patch", 1),  # https://codereview.qt-project.org/#/c/141254/
                    # https://codereview.qt-project.org/#/c/149550/
                    ("qdbus-manager-quit-5.7.patch", 1)  # https://phabricator.kde.org/D2545#69186
                ]
            elif qtVer >= CraftVersion("5.7"):
                self.patchToApply[ver] = [
                    ("fix-angle-mingw.patch", 1),
                    ("qtbase-5.7.patch", 1),  # https://codereview.qt-project.org/#/c/141254/
                    # https://codereview.qt-project.org/#/c/149550/
                    ("do-not-spawn-console-qprocess-startdetached.patch", 1),
                    # https://codereview.qt-project.org/#/c/162585/
                    ("qdbus-manager-quit-5.7.patch", 1)  # https://phabricator.kde.org/D2545#69186
                ]
            else:
                self.patchToApply[ver] = [
                    ("qmake-fix-install-root.patch", 1),
                    ("qtbase-5.6.patch", 1),  # https://codereview.qt-project.org/#/c/141254/
                    # https://codereview.qt-project.org/#/c/149550/
                    ("do-not-spawn-console-qprocess-startdetached.patch", 1),
                    # https://codereview.qt-project.org/#/c/162585/
                    ("fix-angle-mingw-5.6.2-20161027.diff", 1),
                    ("qdbus-manager-quit-5.7.patch", 1)  # https://phabricator.kde.org/D2545#69186
                ]

        self.patchLevel["5.9.4"] = 3
        self.description = "a cross-platform application framework"

    def setDependencies(self):
        if CraftCore.settings.getboolean("Packager", "UseCache") and not CraftCore.settings.getboolean("QtSDK", "Enabled", False):
            self.buildDependencies["dev-utils/qtbinpatcher"] = None
        self.runtimeDependencies["virtual/base"] = None
        self.buildDependencies["dev-utils/perl"] = None
        self.buildDependencies["dev-utils/winflexbison"] = None
        if not self.options.buildStatic:
            self.runtimeDependencies["libs/openssl"] = None if CraftVersion(self.buildTarget) < CraftVersion("5.10") else "1.1"
            self.runtimeDependencies["libs/dbus"] = None
            self.runtimeDependencies["binary/mysql"] = None
            self.runtimeDependencies["libs/icu"] = None
            self.runtimeDependencies["libs/zlib"] = None


class QtPackage(Qt5CorePackageBase):
    def __init__(self, **args):
        Qt5CorePackageBase.__init__(self)

    def compile(self):
        with self.getQtBaseEnv():
            return Qt5CorePackageBase.compile(self)

    def configure(self, unused1=None, unused2=""):
        if CraftCore.compiler.isMinGW() and "DXSDK_DIR" not in os.environ:
            CraftCore.log.critical("Failed to detec a DirectX SDK")
            CraftCore.log.critical(
                "Please visite https://community.kde.org/Guidelines_and_HOWTOs/Build_from_source/Windows#Direct_X_SDK for instructions")
            return False
        self.enterBuildDir()
        if OsUtils.isWin():
            configure = OsUtils.toUnixPath(os.path.join(self.sourceDir(), "configure.bat"))
            if self.qtVer < CraftVersion("5.10"):
                # not needed anymore as we don't patch configure anymore
                if not os.path.exists(os.path.join(self.sourceDir(), ".gitignore")):  # force bootstrap of configure.exe
                    with open(os.path.join(self.sourceDir(), ".gitignore"), "wt+") as bootstrap:
                        bootstrap.write("Force Bootstrap")
                    if os.path.exists(os.path.join(self.sourceDir(), "configure.exe")):
                        os.remove(os.path.join(self.sourceDir(), "configure.exe"))
        elif OsUtils.isUnix():
            configure = os.path.join(self.sourceDir(), "configure")

        command = " %s -opensource  -confirm-license -prefix %s -platform %s " % (
        configure, CraftStandardDirs.craftRoot(), self.platform)
        command += "-headerdir %s " % os.path.join(CraftStandardDirs.craftRoot(), "include", "qt5")
        command += "-qt-libpng "
        command += "-qt-libjpeg "
        # can we drop that in general?
        version = CraftVersion(self.subinfo.buildTarget)
        if version <= CraftVersion("5.6"):
            command += "-c++11 "
        if version >= CraftVersion("5.8"):
            command += "-mp "
        else:
            command += "-qt-pcre "
        if OsUtils.isWin():
            command += "-opengl dynamic "
            command += "-plugin-sql-odbc "
        # if not (OsUtils.isFreeBSD() or compiler.isMinGW()):#currently breaks unmaintained modules like qtscript and webkit
        #    command += "-ltcg "
        if self.buildType() == "RelWithDebInfo":
            command += "-force-debug-info "
        if self.buildType() == "Debug":
            command += "-debug "
        else:
            command += "-release "

        if not self.subinfo.options.buildStatic:
            command += "-I \"%s\" -L \"%s\" " % (
            os.path.join(CraftStandardDirs.craftRoot(), "include"), os.path.join(CraftStandardDirs.craftRoot(), "lib"))
            if self.subinfo.options.isActive("libs/openssl"):
                command += " -openssl-linked "
                if self.qtVer >= CraftVersion("5.10"):
                    opensslIncDir = os.path.join(CraftCore.standardDirs.craftRoot(), "include", "openssl")
                    command += f" OPENSSL_LIBS=\"-llibssl -llibcrypto\" OPENSSL_INCDIR=\"{opensslIncDir}\" "
            if self.subinfo.options.isActive("binary/mysql"):
                command += " -plugin-sql-mysql "
            if self.subinfo.options.isActive("libs/dbus"):
                command += " -qdbus -dbus-runtime -I \"%s\" -I \"%s\" " % (
                os.path.join(CraftStandardDirs.craftRoot(), "include", "dbus-1.0"),
                os.path.join(CraftStandardDirs.craftRoot(), "lib", "dbus-1.0", "include"))
            if self.subinfo.options.isActive("libs/icu"):
                command += " -icu "
            if self.subinfo.options.isActive("libs/zlib"):
                command += " -system-zlib "
                if CraftCore.compiler.isMSVC():
                    command += " ZLIB_LIBS=zlib.lib "
        else:
            command += " -static -static-runtime "

        command += "-nomake examples "
        command += "-nomake tests "

        if (CraftCore.compiler.isMSVC() and CraftCore.compiler.isClang()) or OsUtils.isUnix() or self.supportsCCACHE:
            command += "-no-pch "

        if CraftCore.compiler.isMinGW() and self.qtVer < CraftVersion("5.10"):
            command += """ "QMAKE_CXXFLAGS += -Wa,-mbig-obj" """

        return utils.system(command)

    def install(self):
        with self.getQtBaseEnv():
            if not Qt5CorePackageBase.install(self):
                return False
            utils.copyFile(os.path.join(self.buildDir(), "bin", "qt.conf"),
                           os.path.join(self.imageDir(), "bin", "qt.conf"))

            # install msvc debug files if available
            if CraftCore.compiler.isMSVC():
                srcdir = os.path.join(self.buildDir(), "lib")
                destdir = os.path.join(self.installDir(), "lib")

                filelist = os.listdir(srcdir)

                for file in filelist:
                    if file.endswith(".pdb"):
                        utils.copyFile(os.path.join(srcdir, file), os.path.join(destdir, file))

            return True

    def qmerge(self):
        if OsUtils.isWin() and CraftCore.settings.getboolean("Packager", "UseCache"):
            if not utils.system(["qtbinpatcher", "--nobackup",
                                 f"--qt-dir={self.installDir()}",
                                 f"--new-dir={CraftStandardDirs.craftRoot()}"]):
                return False
        return super().qmerge()

    def getQtBaseEnv(self):
        envs = {}
        envs["PATH"] = os.pathsep.join([os.path.join(self.buildDir(), "bin"), os.environ["PATH"]])
        if CraftVersion(self.subinfo.buildTarget) < CraftVersion("5.9"):
            # so that the mkspecs can be found, when -prefix is set
            envs["QMAKEPATH"] = self.sourceDir()
        if CraftVersion(self.subinfo.buildTarget) < CraftVersion("5.8"):
            envs["QMAKESPEC"] = os.path.join(self.sourceDir(), 'mkspecs', self.platform)
        else:
            envs["QMAKESPEC"] = None
        return utils.ScopedEnv(envs)


class Package(Qt5CoreSdkPackageBase):
    def __init__(self):
        Qt5CoreSdkPackageBase.__init__(self, classA=QtPackage)
