import multiprocessing
import os
from pathlib import Path

import info
import utils
from Blueprints.CraftPackageObject import CraftPackageObject
from Blueprints.CraftVersion import CraftVersion
from CraftCore import CraftCore
from Utils.CraftShortPath import CraftShortPath


class subinfo(info.infoclass):
    def registerOptions(self):
        self.parent.package.categoryInfo.platforms &= CraftCore.compiler.Platforms.Native
        self.options.dynamic.registerOption("withICU", self.options.isActive("libs/icu"))
        self.options.dynamic.registerOption("withHarfBuzz", self.options.isActive("libs/harfbuzz"))

    def setTargets(self):
        self.versionInfo.setDefaultValues()
        self.patchLevel["6.4.0"] = 1
        self.patchToApply["6.5.3"] = [(".6.5.3", 1)]
        self.patchToApply["6.6.0"] = [(".6.5.3", 1)]
        self.patchLevel["6.7.0"] = 3

        for ver in ["6.6.1", "6.6.2"]:
            self.patchToApply[ver] = [
                # don't confuse gn
                ("qtwebengine-6.6.1-20240105.diff", 1),
            ]

        self.patchToApply["6.6.1"] += [
            # QTBUG-120229
            # while the patch is undocumented it apparently fixes
            # qtwebengine-everywhere-src-6.6.1\src\3rdparty\chromium\third_party\highway\src\hwy\ops\emu128-inl.h(69) : fatal error C1002: compiler is out of heap space in pass 2
            ("msvc-template.patch", 1),
            # https://codereview.qt-project.org/c/qt/qtwebengine-chromium/+/528036
            ("chromium-119.0.6045.159-icu-74.patch", 1),
        ]

        # https://invent.kde.org/qt/qt/qtwebengine-chromium/-/commit/3aba63e62a86aeb157ad73df0fe0f44f01cf0e02
        self.patchToApply["6.7.2"] = [("3aba63e62a86aeb157ad73df0fe0f44f01cf0e02.patch", 1)]

        # https://bugreports.qt.io/browse/QTBUG-128907
        self.patchToApply["6.8.0"] = [("bfeea6231dfacb37de3ca5ee2e0167c71b540b90.patch", 1)]

        self.patchLevel["6.6.1"] = 1

    def setDependencies(self):
        self.buildDependencies["dev-utils/gperf"] = None
        self.buildDependencies["dev-utils/flexbison"] = None
        self.buildDependencies["dev-utils/nodejs"] = None
        self.buildDependencies["python-modules/html5lib"] = None

        if CraftCore.compiler.compiler.isMSVC:
            self.buildDependencies["libs/llvm"] = None

        self.runtimeDependencies["libs/qt6/qtbase"] = None
        self.runtimeDependencies["libs/qt6/qtdeclarative"] = None
        self.runtimeDependencies["libs/qt6/qtpositioning"] = None
        self.buildDependencies["libs/qt6/qttools"] = None
        self.runtimeDependencies["libs/qt6/qtwebchannel"] = None
        self.runtimeDependencies["libs/nss"] = None
        self.runtimeDependencies["libs/cups"] = None
        self.runtimeDependencies["libs/libxml2"] = None
        self.runtimeDependencies["libs/libjpeg-turbo"] = None
        self.runtimeDependencies["libs/webp"] = None
        self.runtimeDependencies["libs/zlib"] = None
        self.runtimeDependencies["libs/libpng"] = None
        self.runtimeDependencies["libs/tiff"] = None
        self.runtimeDependencies["libs/lcms2"] = None

        if self.options.dynamic.withICU and CraftCore.compiler.isLinux:
            self.runtimeDependencies["libs/icu"] = None
        if self.options.dynamic.withHarfBuzz:
            self.runtimeDependencies["libs/harfbuzz"] = None


class Package(CraftPackageObject.get("libs/qt6").pattern):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # together with the patch based on https://gitweb.gentoo.org/repo/gentoo.git/tree/dev-qt/qtwebengine/qtwebengine-6.5.2-r1.ebuild

        # use a short path for Windows
        shortDevUtils = CraftShortPath(Path(CraftCore.standardDirs.craftRoot()) / "dev-utils/").shortPath
        self.subinfo.options.configure.args += [
            # no idea why cmake ignores the path env
            f"-DPython3_EXECUTABLE={shortDevUtils / 'bin/python3'}{CraftCore.compiler.platform.executableSuffix}",
            "-DQT_FEATURE_qtwebengine_build=ON",
            # Package harfbuzz-subset was not found
            # f"-DQT_FEATURE_webengine_system_harfbuzz={self.subinfo.options.dynamic.withHarfBuzz.asOnOff}",
            "-DQT_FEATURE_webengine_system_libwebp=ON",
            "-DQT_FEATURE_webengine_system_libjpeg=ON",
            "-DQT_FEATURE_webengine_system_libxml=ON",
            "-DQT_FEATURE_webengine_system_freetype=ON",
            "-DQT_FEATURE_webengine_system_glib=ON",
            "-DQT_FEATURE_webengine_system_lcms2=ON",
            "-DQT_FEATURE_webengine_system_pulseaudio=OFF",
        ]
        # See https://bugs.kde.org/show_bug.cgi?id=486905 and https://github.com/Homebrew/homebrew-core/issues/104008 :
        # option not correctly supported on Windows and MacOS (as of Qt 6.7.0)
        if CraftCore.compiler.isLinux:
            self.subinfo.options.configure.args += [f"-DQT_FEATURE_webengine_system_icu={self.subinfo.options.dynamic.withICU.asOnOff}"]
        else:
            self.subinfo.options.configure.args += ["-DQT_FEATURE_webengine_system_icu=OFF"]

        if CraftCore.compiler.compiler.isMSVC and CraftVersion(self.buildTarget) < CraftVersion("6.7.0"):
            self.subinfo.options.configure.args += [
                "-DCMAKE_CXX_COMPILER=clang-cl",
                "-DCMAKE_C_COMPILER=clang-cl",
                "-DCMAKE_C_LINK_EXECUTABLE=lld-link",
                "-DCMAKE_CXX_LINK_EXECUTABLE=lld-link",
            ]

        if (
            (CraftCore.compiler.isMacOS and CraftVersion(self.buildTarget) >= CraftVersion("6.5.2") and CraftVersion(self.buildTarget) < CraftVersion("6.6.2"))
            # macOS is fixed with 6.6.2, Windows still not :-(
            or CraftCore.compiler.isWindows
        ):
            # See https://bugreports.qt.io/browse/QTBUG-115357
            self.subinfo.options.configure.args += ["-DQT_FEATURE_webengine_system_libpng=OFF"]
        else:
            self.subinfo.options.configure.args += ["-DQT_FEATURE_webengine_system_libpng=ON"]

        if CraftCore.compiler.compiler.isMSVC and CraftVersion(self.buildTarget) >= CraftVersion("6.6.0"):
            self.subinfo.options.configure.args += ["-DQT_FEATURE_webengine_system_zlib=OFF"]
        else:
            self.subinfo.options.configure.args += ["-DQT_FEATURE_webengine_system_zlib=ON"]

    def _getEnv(self):
        # webengine requires enormous amounts of ram
        jobs = int(CraftCore.settings.get("Compile", "Jobs", multiprocessing.cpu_count()))
        env = {"NINJAFLAGS": f"-j{int(jobs/2)}"}
        if CraftCore.compiler.isLinux:
            # this build system is broken and ignore ldflags
            env["LD_LIBRARY_PATH"] = CraftCore.standardDirs.craftRoot() / "lib"
        return env

    def configure(self):
        with utils.ScopedEnv(self._getEnv()):
            return super().configure()

    def make(self):
        with utils.ScopedEnv(self._getEnv()):
            return super().make()

    def install(self):
        if not super().install():
            return False

        if CraftCore.compiler.isWindows and os.path.isdir(self.imageDir() / "resources"):
            # move webengine resource files into location where they will still be found after deplyoment
            # see https://doc.qt.io/qt-6/qtwebengine-deploying.html for lookup rules
            if not utils.mergeTree(self.imageDir() / "resources", self.imageDir() / "bin"):
                return False

        return True
