# -*- coding: utf-8 -*-

import info
from Package.Qt5CorePackageBase import *


class subinfo(info.infoclass):
    def registerOptions(self):
        self.options.dynamic.registerOption("buildCommercial", False)
        self.options.dynamic.registerOption("buildReleaseAndDebug", False)
        self.options.dynamic.registerOption("buildDoc", True)
        self.options.dynamic.registerOption("libInfix", "")

    def setTargets(self):
        self.versionInfo.setDefaultValues()

        for ver in self.versionInfo.tarballs() + self.versionInfo.branches() + self.versionInfo.tags():
            qtVer = CraftVersion(ver)
            if ver == "dev":
                self.patchToApply[ver] = []
            elif qtVer >= CraftVersion("5.12.4"):
                raise Exception("check patches!")# recheck
            elif qtVer >= CraftVersion("5.12.1"):
                self.patchToApply[ver] = [
                    ("qdbus-manager-quit-5.7.patch", 1),  # https://phabricator.kde.org/D2545#69186
                    ("workaround-mingw-egl.diff", 1),
                    ("fix_GenericDataLocation_mac.patch", 1),
                    ("qstandardpaths-extra-dirs.patch", 1),
                    ("qtbase-5.12.3-macos-debug.diff", 1) # https://codereview.qt-project.org/c/qt/qtbase/+/260917
                ]
            elif qtVer >= CraftVersion("5.12.0"):
                self.patchToApply[ver] = [
                    ("qdbus-manager-quit-5.7.patch", 1),  # https://phabricator.kde.org/D2545#69186
                    ("workaround-mingw-egl.diff", 1),
                    ("fix_GenericDataLocation_mac.patch", 1),
                    ("qstandardpaths-extra-dirs.patch", 1),
                    ("0001-QComboBox-WindowVistaStyle-restore-focus-rect.patch", 1), # https://codereview.qt-project.org/#/c/248945/
                    (".qt-5.12.0", 1)
                ]
            elif qtVer >= CraftVersion("5.11.1"):
                self.patchToApply[ver] = [
                    ("qdbus-manager-quit-5.7.patch", 1),  # https://phabricator.kde.org/D2545#69186
                    ("workaround-mingw-egl.diff", 1),
                    ("fix_GenericDataLocation_mac.patch", 1),
                    ("qstandardpaths-extra-dirs.patch", 1),
                ]
            elif qtVer >= CraftVersion("5.11"):
                self.patchToApply[ver] = [
                    ("qdbus-manager-quit-5.7.patch", 1), # https://phabricator.kde.org/D2545#69186
                    ("0001-Fix-private-headers.patch", 1),  # https://bugreports.qt.io/browse/QTBUG-37417
                    ("workaround-mingw-egl.diff", 1),
                    ("fix_GenericDataLocation_mac.patch", 1),
                    ("qstandardpaths-extra-dirs.patch", 1),
                ]
            elif qtVer >= CraftVersion("5.10"):
                self.patchToApply[ver] = [
                    ("qdbus-manager-quit-5.7.patch", 1), # https://phabricator.kde.org/D2545#69186
                    ("0001-Fix-private-headers.patch", 1),  # https://bugreports.qt.io/browse/QTBUG-37417
                    ("workaround-mingw-egl.diff", 1),
                    ("fix_AppDataLocation_mac.patch", 1), #https://bugreports.qt.io/browse/QTBUG-61159
                    ("fix_GenericDataLocation_mac.patch", 1),
                    ("qstandardpaths-extra-dirs.patch", 1),
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

        self.patchToApply["5.11.2"] += [
            ("0001-Export-qt_open64-from-QtCore.patch", 1), # fix 32 bit unix builds, backport of 4fc4f7b0ce0e6ee186a7d7fe9b5dd20e94efe432
        ]

        self.patchLevel["5.9.4"] = 3
        self.patchLevel["5.11.0"] = 2
        self.patchLevel["5.11.2"] = 3
        self.patchLevel["5.12.0"] = 2
        self.patchLevel["5.12.1"] = 2
        self.patchLevel["5.12.3"] = 1
        self.description = "a cross-platform application framework"

    def setDependencies(self):
        if CraftCore.settings.getboolean("Packager", "UseCache") and not CraftCore.settings.getboolean("QtSDK", "Enabled", False):
            self.buildDependencies["dev-utils/qtbinpatcher"] = None
        self.runtimeDependencies["virtual/base"] = None
        self.buildDependencies["dev-utils/perl"] = None
        self.buildDependencies["dev-utils/flexbison"] = None
        if not self.options.buildStatic:
            if CraftVersion(self.buildTarget) < CraftVersion("5.10") or CraftCore.settings.getboolean("QtSDK", "Enabled", False):
                self.runtimeDependencies["libs/openssl"] = None
            else:
                self.runtimeDependencies["libs/openssl"] = "1.1"
            self.runtimeDependencies["libs/dbus"] = None
            self.runtimeDependencies["binary/mysql"] = None
            self.runtimeDependencies["libs/icu"] = None
            self.runtimeDependencies["libs/zlib"] = None


class QtPackage(Qt5CorePackageBase):
    def __init__(self, **args):
        Qt5CorePackageBase.__init__(self)

    def configure(self, unused1=None, unused2=""):
        with self.getQtBaseEnv():
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

            command = f"{configure} -confirm-license -prefix {CraftStandardDirs.craftRoot()} -platform {self.platform} "
            command += "-opensource " if not self.subinfo.options.dynamic.buildCommercial else "-commercial "
            if self.subinfo.options.dynamic.libInfix:
                command += f"-qtlibinfix {self.subinfo.options.dynamic.libInfix} "
            command += f"-headerdir {os.path.join(CraftStandardDirs.craftRoot(), 'include', 'qt5')} "
            command += "-qt-libpng "
            command += "-qt-libjpeg "

            # can we drop that in general?
            if self.qtVer <= "5.6":
                command += "-c++11 "
            if self.qtVer >= "5.8":
                command += "-mp "
            else:
                command += "-qt-pcre "

            if CraftCore.compiler.isMacOS and self.qtVer >= "5.10":
                command += f"-macos-additional-datadirs \"{CraftCore.standardDirs.locations.data}\" "

            if OsUtils.isWin():
                command += "-opengl dynamic "
                command += "-plugin-sql-odbc "

            # if not (OsUtils.isFreeBSD() or compiler.isMinGW()):#currently breaks unmaintained modules like qtscript and webkit
            #    command += "-ltcg "

            if self.subinfo.options.dynamic.buildReleaseAndDebug:
                command += "-debug-and-release "
            elif self.buildType() == "Debug":
                command += "-debug "
            else:
                command += "-release "

            if self.buildType() == "RelWithDebInfo":
                command += "-force-debug-info "

            if not self.subinfo.options.dynamic.buildReleaseAndDebug:
                if self.buildType() == "Debug" and CraftCore.compiler.isMacOS:
                    command += "-no-framework "

            if not self.subinfo.options.buildStatic:
                command += "-I \"%s\" -L \"%s\" " % (
                    os.path.join(CraftStandardDirs.craftRoot(), "include"), os.path.join(CraftStandardDirs.craftRoot(), "lib"))
                if self.subinfo.options.isActive("libs/openssl"):
                    command += " -openssl-linked "
                    if self.qtVer >= CraftVersion("5.10"):
                        opensslIncDir = os.path.join(CraftCore.standardDirs.craftRoot(), "include", "openssl")
                        command += f" OPENSSL_INCDIR=\"{opensslIncDir}\""
                        if CraftCore.compiler.isWindows:
                            command += f" OPENSSL_LIBS=\"-llibssl -llibcrypto\" "
                        else:
                            command += f" OPENSSL_LIBS=\"-lssl -lcrypto\" "
                if self.subinfo.options.isActive("binary/mysql"):
                    command += " -sql-mysql "
                if self.subinfo.options.isActive("libs/dbus"):
                    command += " -qdbus -dbus-runtime -I \"%s\" -I \"%s\" " % (
                        os.path.join(CraftStandardDirs.craftRoot(), "include", "dbus-1.0"),
                        os.path.join(CraftStandardDirs.craftRoot(), "lib", "dbus-1.0", "include"))
                else:
                    command += " -no-dbus "
                if self.subinfo.options.isActive("libs/icu"):
                    command += " -icu "
                else:
                    command += " -no-icu "
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
            if CraftCore.compiler.isLinux:
                command += """-R "../lib" """

            if CraftCore.compiler.isMinGW() and self.qtVer < "5.10":
                command += """ "QMAKE_CXXFLAGS += -Wa,-mbig-obj" """

            return utils.system(command)


    def make(self):
        with self.getQtBaseEnv():
            return super().make()

    def install(self):
        with self.getQtBaseEnv():
            if not Qt5CorePackageBase.install(self):
                return False
            parser = configparser.ConfigParser()
            parser.optionxform = str
            parser.read(os.path.join(self.buildDir(), "bin", "qt.conf"))
            parser.remove_section("EffectiveSourcePaths")
            with open(os.path.join(self.imageDir(), "bin", "qt.conf"), "wt") as out:
                parser.write(out)
            return True

    def postInstall(self):
        if CraftCore.compiler.isWindows and CraftCore.settings.getboolean("Packager", "UseCache"):
            return utils.system(["qtbinpatcher", "--nobackup",
                                 f"--qt-dir={self.installDir()}",
                                 f"--new-dir={CraftStandardDirs.craftRoot()}"])
        else:
            return self.patchInstallPrefix([os.path.join(self.installDir(), "bin", "qt.conf")],
                                           self.subinfo.buildPrefix,
                                           CraftCore.standardDirs.craftRoot())

    def getQtBaseEnv(self):
        envs = {}
        envs["PATH"] = os.pathsep.join([os.path.join(self.buildDir(), "bin"), os.environ["PATH"]])
        if self.qtVer < "5.9":
            # so that the mkspecs can be found, when -prefix is set
            envs["QMAKEPATH"] = self.sourceDir()
        if self.qtVer < "5.8":
            envs["QMAKESPEC"] = os.path.join(self.sourceDir(), 'mkspecs', self.platform)
        else:
            envs["QMAKESPEC"] = None
        return utils.ScopedEnv(envs)


class Package(Qt5CoreSdkPackageBase):
    def __init__(self):
        Qt5CoreSdkPackageBase.__init__(self, classA=QtPackage)
