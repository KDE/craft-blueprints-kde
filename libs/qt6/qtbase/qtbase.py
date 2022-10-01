import os

from CraftCore import CraftCore
import info
import utils

class subinfo(info.infoclass):
    def registerOptions(self):
        self.options.dynamic.registerOption("buildCommercial", False)
        self.options.dynamic.registerOption("buildReleaseAndDebug", False)
        self.options.dynamic.registerOption("libInfix", "")
        self.options.dynamic.registerOption("useLtcg", False)
        self.options.dynamic.registerOption("withDBus", True)
        self.options.dynamic.registerOption("withGlib", not CraftCore.compiler.isWindows)

    def setTargets(self):
        self.versionInfo.setDefaultValues()

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
            self.runtimeDependencies["libs/zlib"] = None
            self.runtimeDependencies["libs/libzstd"] = None
            self.runtimeDependencies["libs/libpng"] = None
            self.runtimeDependencies["libs/libjpeg-turbo"] = None
            self.runtimeDependencies["libs/sqlite"] = None
            self.runtimeDependencies["libs/pcre2"] = None
            self.runtimeDependencies["libs/harfbuzz"] = None
            self.runtimeDependencies["libs/freetype"] = None
            if CraftCore.compiler.isUnix and self.options.dynamic.withGlib:
                self.runtimeDependencies["libs/glib"] = None


from Package.CMakePackageBase import *
class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)

        self.subinfo.options.configure.args += [
            "-DFEATURE_pkg_config=ON",
            
            "-DFEATURE_system_sqlite=ON",
            "-DFEATURE_system_pcre2=ON",
            "-DFEATURE_system_zlib=ON",
            "-DFEATURE_system_harfbuzz=ON",
            "-DFEATURE_system_freetype=ON",

            "-DFEATURE_openssl_linked=ON",

            "-DQT_BUILD_EXAMPLES=OFF"
        ]

        if self.subinfo.options.dynamic.useLtcg:
            self.subinfo.options.configure.args += ["-DCMAKE_INTERPROCEDURAL_OPTIMIZATION=ON"]
