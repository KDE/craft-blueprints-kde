# -*- coding: utf-8 -*-
import info


class subinfo(info.infoclass):
    def registerOptions(self):
        # only supports msvc17+
        if CraftCore.compiler.isMSVC() and CraftCore.compiler.getInternalVersion() < 15:
            self.parent.package.categoryInfo.compiler = CraftCore.compiler.Compiler.NoCompiler
        elif CraftCore.compiler.isMinGW():
            self.parent.package.categoryInfo.compiler = CraftCore.compiler.Compiler.NoCompiler


    def setTargets(self):
        self.versionInfo.setDefaultValues()
        self.patchLevel["5.12.1"] = 2

        self.patchToApply["5.12.3"] = [("0001-Fix-building-GN-with-VS-2019.patch", 1),
                                       ("c6fb532d81f405b2456c382aa0b29eef8866f993.patch", 1)]
        self.patchToApply["5.13.0"] = [("20b5e27.diff", 1)]

        # reduce windows debug lvl to prevent out of memory during linking
        self.patchToApply["5.13.2"] = [("qtwebengine-5.13.2-20191124.diff", 1)]
        self.patchToApply["5.14.0"] = [("harfbuzz-2.6.1-gcc-9.patch", 1)] # https://gitweb.gentoo.org/repo/gentoo.git/plain/media-libs/harfbuzz/files/harfbuzz-2.6.1-gcc-9.patch?id=5e2c1c13fa388533d075554da87d3641019aa739
        self.patchToApply["5.14.1"] = [("harfbuzz-2.6.1-gcc-9.patch", 1), # https://gitweb.gentoo.org/repo/gentoo.git/plain/media-libs/harfbuzz/files/harfbuzz-2.6.1-gcc-9.patch?id=5e2c1c13fa388533d075554da87d3641019aa739
                                       ("qtwebengine-5.14.1-20200227.diff", 1)]
        self.patchToApply["5.15.0"] = [
                (".qt-5.15.0", 1)
        ]


    def setDependencies(self):
        self.buildDependencies["dev-utils/gperf"] = None
        self.buildDependencies["dev-utils/flexbison"] = None
        self.buildDependencies["dev-utils/python2"] = None
        self.runtimeDependencies["libs/qt5/qtbase"] = None
        self.runtimeDependencies["libs/qt5/qtlocation"] = None
        self.runtimeDependencies["libs/qt5/qtdeclarative"] = None
        self.runtimeDependencies["libs/qt5/qtwebchannel"] = None
        if not CraftCore.compiler.isWindows:
            self.runtimeDependencies["libs/lcms2"] = None
            self.runtimeDependencies["libs/freetype"] = None
            self.runtimeDependencies["libs/libopus"] = None
            self.runtimeDependencies["libs/zlib"] = None
            self.runtimeDependencies["libs/libxml2"] = None
            self.runtimeDependencies["libs/libxslt"] = None
            self.runtimeDependencies["libs/freetype"] = None
            self.runtimeDependencies["libs/fontconfig"] = None
            self.runtimeDependencies["libs/libjpeg-turbo"] = None
            self.runtimeDependencies["qt-libs/poppler"] = None
            self.runtimeDependencies["libs/webp"] = None
            self.runtimeDependencies["libs/ffmpeg"] = None


from Package.Qt5CorePackageBase import *


class QtPackage(Qt5CorePackageBase):
    def __init__(self, **args):
        Qt5CorePackageBase.__init__(self)
        self.subinfo.options.fetch.checkoutSubmodules = True
        if CraftCore.compiler.isLinux:
            self.subinfo.options.configure.args += " -- --webengine-pulseaudio=no --webengine-ffmpeg=system --webengine-icu=system"

    def fetch(self):
        if isinstance(self, GitSource):
            utils.system(["git", "clean", "-xdf"], cwd=self.sourceDir())
        return super().fetch()

    def _getEnv(self):
        env = {
            "BISON_PKGDATADIR": None,
            "NINJAFLAGS": " "  # if this is not set qmake will do a verbose mode
        }
        if CraftCore.compiler.isMacOS:
            # we need mac's version of libtool here
            env["PATH"] = f"/usr/bin/:{os.environ['PATH']}"
        if CraftCore.compiler.isWindows:
            # shorten the path to python2 which is passed to gn...
            shortDevUtils = CraftShortPath(Path(CraftCore.standardDirs.craftRoot()) / "dev-utils/bin").shortPath
            env["PATH"] = f"{shortDevUtils};{os.environ['PATH']}"
        return env

    def configure(self, configureDefines=""):
        with utils.ScopedEnv(self._getEnv()):
            return super().configure()

    def make(self):
        with utils.ScopedEnv(self._getEnv()):
            return super().make()

    def install(self):
        if not super().install():
            return False

        if CraftCore.compiler.isWindows and os.path.isdir(os.path.join(self.imageDir(), "resources")):
            # apply solution for wrong install location of some important files
            # see: https://stackoverflow.com/a/35448081
            utils.mergeTree(os.path.join(self.imageDir(), "resources"),
                            os.path.join(self.imageDir(), "bin"))
        return True


class Package(Qt5CoreSdkPackageBase):
    def __init__(self):
        Qt5CoreSdkPackageBase.__init__(self, classA=QtPackage)
