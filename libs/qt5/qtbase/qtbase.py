# -*- coding: utf-8 -*-

import info
from Package.Qt5CorePackageBase import *


class subinfo(info.infoclass):
    def registerOptions(self):
        self.options.dynamic.registerOption("buildCommercial", False)
        self.options.dynamic.registerOption("buildReleaseAndDebug", False)
        self.options.dynamic.registerOption("buildDoc", True)
        self.options.dynamic.registerOption("libInfix", "")
        self.options.dynamic.registerOption("useLtcg", False)
        self.options.dynamic.registerOption("withMysql", not CraftCore.compiler.isMacOS)
        self.options.dynamic.registerOption("withDBus", True)
        self.options.dynamic.registerOption("withGlib", not CraftCore.compiler.isWindows)

    def setTargets(self):
        self.versionInfo.setDefaultValues()

        for ver in self.versionInfo.tarballs() + self.versionInfo.branches() + self.versionInfo.tags():
            qtVer = CraftVersion(ver)
            if ver == "dev":
                self.patchToApply[ver] = []
            if qtVer >= "5.15.0":
                self.patchToApply[ver] = [
                    (".qt-5.15.0", 1)
                ]
            elif qtVer >= CraftVersion("5.12.10"):
                self.patchToApply[ver] = [
                    (".qt-5.12.10", 1)
                ]
            elif qtVer >= CraftVersion("5.12.9"):
                self.patchToApply[ver] = [
                    (".qt-5.12.9", 1)
                ]
            elif qtVer >= CraftVersion("5.12.7"):
                self.patchToApply[ver] = [
                    ("8a3fde00bf53d99e9e4853e8ab97b0e1bcf74915.patch", 1), # https://github.com/qt/qtbase/commit/8a3fde00bf53d99e9e4853e8ab97b0e1bcf74915
                    ("qdbus-manager-quit-5.7.patch", 1),  # https://phabricator.kde.org/D2545#69186
                    ("workaround-mingw-egl.diff", 1),
                    ("fix_GenericDataLocation_mac.patch", 1),
                    ("qstandardpaths-extra-dirs.patch", 1),
                    ("qtbase-5.13.1-20191104.diff", 1)  # https://bugreports.qt.io/browse/QTBUG-72846
                ]
            elif qtVer >= CraftVersion("5.12.4"):
                self.patchToApply[ver] = [
                    ("qdbus-manager-quit-5.7.patch", 1),  # https://phabricator.kde.org/D2545#69186
                    ("workaround-mingw-egl.diff", 1),
                    ("fix_GenericDataLocation_mac.patch", 1),
                    ("qstandardpaths-extra-dirs.patch", 1),
                    ("qtbase-5.13.1-20191104.diff", 1)  # https://bugreports.qt.io/browse/QTBUG-72846
                ]
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

        self.patchLevel["5.12.0"] = 2
        self.patchLevel["5.12.1"] = 2
        self.patchLevel["5.12.3"] = 1
        self.patchLevel["5.12.9"] = 1
        self.patchLevel["5.12.10"] = 1
        self.patchLevel["5.15.0"] = 4
        self.patchLevel["5.15.1"] = 4
        self.description = "a cross-platform application framework"

    def setDependencies(self):
        if CraftCore.settings.getboolean("Packager", "UseCache") and not CraftCore.settings.getboolean("QtSDK", "Enabled", False):
            self.buildDependencies["dev-utils/qtbinpatcher"] = None
        self.runtimeDependencies["virtual/base"] = None
        self.buildDependencies["dev-utils/pkg-config"] = None
        self.buildDependencies["dev-utils/perl"] = None
        self.buildDependencies["dev-utils/flexbison"] = None
        if not self.options.buildStatic:
            if CraftCore.settings.getboolean("QtSDK", "Enabled", False):
                self.runtimeDependencies["libs/openssl"] = None
            else:
                self.runtimeDependencies["libs/openssl"] = "1.1"
            if self.options.dynamic.withDBus:
                self.runtimeDependencies["libs/dbus"] = None
            if self.options.dynamic.withMysql:
                self.runtimeDependencies["binary/mysql"] = None
            self.runtimeDependencies["libs/icu"] = None
            self.runtimeDependencies["libs/zlib"] = None
            self.runtimeDependencies["libs/libzstd"] = None
            self.runtimeDependencies["libs/libpng"] = None
            self.runtimeDependencies["libs/libjpeg-turbo"] = None
            self.runtimeDependencies["libs/sqlite"] = None
            self.runtimeDependencies["libs/pcre2"] = None
            if CraftCore.compiler.isUnix and self.options.dynamic.withGlib:
                self.runtimeDependencies["libs/glib"] = None


class QtPackage(Qt5CorePackageBase):
    def __init__(self, **args):
        Qt5CorePackageBase.__init__(self)

    def configure(self, unused1=None, unused2=""):
        # https://github.com/qt/qtbase/blob/5.14/mkspecs/common/macx.conf#L8
        if CraftCore.compiler.isMacOS:
            if self.qtVer >= "5.14":
                mac_required = "10.13"
            elif self.qtVer >= "5.12":
                mac_required = "10.12"
            if not CraftVersion(os.environ["MACOSX_DEPLOYMENT_TARGET"]) >= mac_required:
                raise BlueprintException(f"Qt requires MACOSX_DEPLOYMENT_TARGET to be >= {mac_required}", self)
        with self.getQtBaseEnv():
            if CraftCore.compiler.isMinGW() and "DXSDK_DIR" not in os.environ:
                CraftCore.log.critical("Failed to detec a DirectX SDK")
                CraftCore.log.critical(
                    "Please visite https://community.kde.org/Guidelines_and_HOWTOs/Build_from_source/Windows#Direct_X_SDK for instructions")
                return False
            self.enterBuildDir()
            if OsUtils.isWin():
                configure = OsUtils.toUnixPath(os.path.join(self.sourceDir(), "configure.bat"))
            elif OsUtils.isUnix():
                configure = os.path.join(self.sourceDir(), "configure")

            command = f"{configure} -confirm-license -prefix {CraftStandardDirs.craftRoot()} -platform {self.platform} "
            command += "-opensource " if not self.subinfo.options.dynamic.buildCommercial else "-commercial "
            if self.subinfo.options.dynamic.libInfix:
                command += f"-qtlibinfix {self.subinfo.options.dynamic.libInfix} "
            command += f"-headerdir {os.path.join(CraftStandardDirs.craftRoot(), 'include', 'qt5')} "
            command += "-pkg-config "

            if self.subinfo.options.isActive("libs/libpng"):
                command += "-system-libpng "
            else:
                command += "-qt-libpng "
            if self.subinfo.options.isActive("libs/libjpeg-turbo"):
                command += "-system-libjpeg "
            else:
                command += "-qt-libjpeg "
            if self.subinfo.options.isActive("libs/sqlite"):
                command += "-system-sqlite "
            if self.subinfo.options.isActive("libs/pcre2"):
                command += "-system-pcre "
            if self.subinfo.options.isActive("libs/zlib"):
                command += " -system-zlib "
                if CraftCore.compiler.isMSVC():
                    command += " ZLIB_LIBS=zlib.lib "

            command += "-qt-doubleconversion "

            command += "-mp "

            if CraftCore.compiler.isMacOS:
                command += f"-macos-additional-datadirs \"{CraftCore.standardDirs.locations.data}\" "

            if OsUtils.isWin():
                command += "-opengl dynamic "
                command += "-plugin-sql-odbc "

            if self.subinfo.options.dynamic.useLtcg:
                command += "-ltcg "

            if self.subinfo.options.dynamic.buildReleaseAndDebug:
                command += "-debug-and-release "
            elif self.buildType() == "Debug":
                command += "-debug "
            else:
                command += "-release "

            if not CraftCore.compiler.isWindows and self.buildType() != "Release":
                command += "-separate-debug-info "

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
                if self.subinfo.options.dynamic.withMysql:
                    command += " -sql-mysql "
                else:
                    command += " -no-sql-mysql "
                if self.subinfo.options.dynamic.withDBus:
                    command += " -qdbus -dbus-runtime -I \"%s\" -I \"%s\" " % (
                        os.path.join(CraftStandardDirs.craftRoot(), "include", "dbus-1.0"),
                        os.path.join(CraftStandardDirs.craftRoot(), "lib", "dbus-1.0", "include"))
                else:
                    command += " -no-dbus "
                if self.subinfo.options.isActive("libs/icu"):
                    icuIncDir = os.path.join(CraftCore.standardDirs.craftRoot(), "include")
                    command += f" ICU_INCDIR=\"{icuIncDir}\""
                    command += " -icu "
                else:
                    command += " -no-icu "
                if not self.subinfo.options.dynamic.withGlib:
                    command += " -no-glib "
            else:
                command += " -static -static-runtime "

            command += "-nomake examples "
            command += "-nomake tests "

            if (CraftCore.compiler.isMSVC() and CraftCore.compiler.isClang()) or OsUtils.isUnix() or self.supportsCCACHE:
                command += "-no-pch "
            if self.supportsCCACHE:
                command += "-ccache "

            if CraftCore.compiler.isLinux:
                command += """-R "../lib" """
            elif CraftCore.compiler.isMacOS:
                command += f"""-R "{CraftCore.standardDirs.craftRoot()}/lib" """

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
            if not self.patchInstallPrefix([os.path.join(self.installDir(), "bin", "qt.conf")],
                                           self.subinfo.buildPrefix,
                                           CraftCore.standardDirs.craftRoot()):
                return False

        # try to normalize the auto-detected paths during Qt build for non-debian distros
        if CraftCore.compiler.isLinux:
            files = utils.filterDirectoryContent(self.installDir(),
                                             whitelist=lambda x, root: Path(x).suffix in {".cmake", ".prl", ".pri"},
                                             blacklist=lambda x, root: True)
            for f in files:
                with open(f, "rb") as _f:
                    old = _f.read()
                with open(f, "wb") as _f:
                    _f.write(re.sub(rb'/usr/lib/(\w+-\w+-\w+/)?lib(\w+)\.so', rb'-l\2', old))
        return True

    def getQtBaseEnv(self):
        envs = Qt5CoreBuildSystem._qtCoreEnv(self)
        envs["PATH"] = os.pathsep.join([os.path.join(self.buildDir(), "bin"), os.environ["PATH"]])
        envs["QMAKESPEC"] = None
        return utils.ScopedEnv(envs)


class Package(Qt5CoreSdkPackageBase):
    def __init__(self):
        Qt5CoreSdkPackageBase.__init__(self, classA=QtPackage)
