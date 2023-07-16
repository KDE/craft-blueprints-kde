import os

import info
import utils
from CraftCore import CraftCore


class subinfo(info.infoclass):
    def registerOptions(self):
        self.options.dynamic.registerOption("buildCommercial", False)
        self.options.dynamic.registerOption("buildReleaseAndDebug", False)
        self.options.dynamic.registerOption("libInfix", "")
        self.options.dynamic.registerOption("useLtcg", False)
        self.options.dynamic.registerOption("withDBus", not CraftCore.compiler.isAndroid)
        self.options.dynamic.registerOption("withGlib", not CraftCore.compiler.isWindows and not CraftCore.compiler.isAndroid)

    def setTargets(self):
        self.versionInfo.setDefaultValues()
        self.patchToApply["6.4.3"] = [(".craft", 1)]
        self.patchLevel["6.4.3"] = 4
        self.patchToApply["6.5.0"] = [(".craft", 1)]

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.buildDependencies["dev-utils/pkg-config"] = None
        self.buildDependencies["dev-utils/perl"] = None
        self.buildDependencies["dev-utils/flexbison"] = None
        if not self.options.buildStatic:
            self.runtimeDependencies["libs/openssl"] = None
            if self.options.dynamic.withDBus:
                self.runtimeDependencies["libs/dbus"] = None
            self.runtimeDependencies["libs/icu"] = None
            self.runtimeDependencies["libs/brotli"] = None
            self.runtimeDependencies["libs/zlib"] = None
            self.runtimeDependencies["libs/libzstd"] = None
            self.runtimeDependencies["libs/libpng"] = None
            self.runtimeDependencies["libs/libjpeg-turbo"] = None
            self.runtimeDependencies["libs/sqlite"] = None
            self.runtimeDependencies["libs/pcre2"] = None
            self.runtimeDependencies["libs/harfbuzz"] = None
            self.runtimeDependencies["libs/freetype"] = None
            self.runtimeDependencies["libs/fontconfig"] = None
            if CraftCore.compiler.isUnix and self.options.dynamic.withGlib:
                self.runtimeDependencies["libs/glib"] = None


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)

        self.subinfo.options.configure.args += [
            "-DFEATURE_pkg_config=ON",
            "-DFEATURE_system_sqlite=ON",
            "-DFEATURE_system_zlib=ON",
            "-DFEATURE_system_freetype=ON",
            "-DQT_FEATURE_sql_odbc=OFF",
            "-DFEATURE_openssl_linked=ON",
            "-DQT_BUILD_EXAMPLES=OFF",
        ]

        if CraftCore.compiler.isLinux:
            self.subinfo.options.configure.args += ["-DFEATURE_xcb=ON"]

        if self.subinfo.options.isActive("libs/pcre2"):
            self.subinfo.options.configure.args += ["-DFEATURE_system_pcre2=ON"]

        if self.subinfo.options.isActive("libs/icu"):
            self.subinfo.options.configure.args += ["-DFEATURE_icu=ON"]

        if self.subinfo.options.isActive("libs/harfbuzz"):
            self.subinfo.options.configure.args += ["-DFEATURE_system_harfbuzz=ON"]
        if self.subinfo.options.isActive("libs/fontconfig"):
            self.subinfo.options.configure.args += ["-DFEATURE_fontconfig=ON"]

        if not self.subinfo.options.dynamic.withDBus:
            self.subinfo.options.configure.args += ["-DFEATURE_dbus=OFF"]

        if not self.subinfo.options.dynamic.withGlib:
            self.subinfo.options.configure.args += ["-DFEATURE_glib=OFF"]

        if CraftCore.compiler.isAndroid:
            self.subinfo.options.configure.args += [f"-DANDROID_ABI={CraftCore.compiler.androidAbi}", "-DECM_THREADS_WORKAROUND=OFF"]

        if self.subinfo.options.dynamic.useLtcg:
            self.subinfo.options.configure.args += ["-DCMAKE_INTERPROCEDURAL_OPTIMIZATION=ON"]
