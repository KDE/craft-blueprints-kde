# -*- coding: utf-8 -*-
import info


class subinfo(info.infoclass):
    def registerOptions(self):
        # only supports msvc17+
        if CraftCore.compiler.isMSVC() and CraftCore.compiler.getInternalVersion() < 15:
            self.parent.package.categoryInfo.compiler = CraftCore.compiler.Compiler.NoCompiler

    def setTargets(self):
        self.versionInfo.setDefaultValues()
        self.patchLevel["5.12.1"] = 2

        self.patchToApply["5.12.3"] = [("0001-Fix-building-GN-with-VS-2019.patch", 1),
                                       ("c6fb532d81f405b2456c382aa0b29eef8866f993.patch", 1)]
        self.patchToApply["5.13.0"] = [("20b5e27.diff", 1)]

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
            self.subinfo.options.configure.args += " -- --webengine-pulseaudio=no --webengine-ffmpeg=system"

    def fetch(self):
        if isinstance(self, GitSource):
            utils.system(["git", "clean", "-xdf"], cwd=self.sourceDir())
        return super().fetch()

    def _getEnv(self):
        env = {
            "BISON_PKGDATADIR": None,
            "NINJAFLAGS": "-j{0}".format(int(CraftCore.settings.get("Compile", "Jobs", multiprocessing.cpu_count()) / 2))
        }
        if CraftCore.compiler.isMacOS:
            # we need mac's version of libtool here
            env["PATH"] = f"/usr/bin/:{os.environ['PATH']}"
        if self.qtVer < CraftVersion("5.9") and CraftCore.compiler.isWindows:
            env["PATH"] = CraftCore.settings.get("Paths", "PYTHON27") + ";" + os.environ["PATH"]
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
        Qt5CoreSdkPackageBase.__init__(self, classA=QtPackage, condition=not CraftCore.compiler.isMinGW())
