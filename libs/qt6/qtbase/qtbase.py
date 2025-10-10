import info
import utils
from Blueprints.CraftPackageObject import CraftPackageObject
from Blueprints.CraftVersion import CraftVersion
from CraftCore import CraftCore


class subinfo(info.infoclass):
    def registerOptions(self):
        self.options.dynamic.registerOption("buildCommercial", False)
        self.options.dynamic.registerOption("buildReleaseAndDebug", False)
        self.options.dynamic.registerOption("libInfix", "")
        self.options.dynamic.registerOption("useLtcg", False)
        self.options.dynamic.registerOption("withDBus", not CraftCore.compiler.isAndroid)
        self.options.dynamic.registerOption("withGlib", not CraftCore.compiler.isWindows and not CraftCore.compiler.isAndroid)
        self.options.dynamic.registerOption("withICU", self.options.isActive("libs/icu"))
        self.options.dynamic.registerOption("withHarfBuzz", self.options.isActive("libs/harfbuzz"))
        self.options.dynamic.registerOption("withPCRE2", self.options.isActive("libs/pcre2"))
        self.options.dynamic.registerOption("withEgl", True)
        self.options.dynamic.registerOption("withCUPS", CraftCore.compiler.isMacOS or self.options.isActive("libs/cups"))

        # We need to treat MacOS explicitly because of https://bugreports.qt.io/browse/QTBUG-116083
        self.options.dynamic.registerOption("withFontConfig", self.options.isActive("libs/fontconfig") and not CraftCore.compiler.isMacOS)

    def setTargets(self):
        self.versionInfo.setDefaultValues()
        for ver in self.targets.keys():
            # These are patches that we can't submit upstream
            # Apply them to all future versions
            self.patchToApply[ver] = [(".craft", 1)]
            if CraftVersion(ver) < "6.9.999999":
                self.patchToApply[ver] = [(".craft_before_6.10", 1)]
            if CraftVersion(ver) < "6.6.999999":
                self.patchToApply[ver] = [(".craft_before_6.7", 1)]

        # backport of https://codereview.qt-project.org/c/qt/qtbase/+/528067
        for ver in ["6.6.0", "6.6.1"]:
            self.patchToApply[ver] += [("android-fix-temporary-content-uri-access.diff", 1)]
        # backport of https://codereview.qt-project.org/c/qt/qtbase/+/537693
        for ver in ["6.6.0", "6.6.1", "6.6.2"]:
            self.patchToApply[ver] += [("android-fix-qtimezone-performance.diff", 1)]

        # https://bugreports.qt.io/browse/QTBUG-129896
        self.patchToApply["6.8.0"] += [("fd484bb.diff", 1)]
        self.patchToApply["6.8.0"] += [("qt680-fix-infinite-icu-loop.diff", 1)]

        # https://bugreports.qt.io/browse/QTBUG-132410 (fixed in 6.8.2)
        if CraftCore.compiler.isAndroid:
            self.patchToApply["6.8.1"] += [("8814bb1e81adcc74f504fb3c7fb1508dff4b68d9.diff", 1), ("0be9ebcc222c14266e6330c58de794d60d6d35ed.diff", 1)]
            self.patchLevel["6.8.1"] = 1

        self.patchLevel["6.4.3"] = 4
        self.patchLevel["6.6.0"] = 4
        self.patchLevel["6.6.1"] = 3
        self.patchLevel["6.8.0"] = 2
        self.patchLevel["6.8.1"] = 2

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.buildDependencies["dev-utils/pkgconf"] = None
        self.buildDependencies["dev-utils/perl"] = None
        self.buildDependencies["dev-utils/flexbison"] = None
        if not self.options.buildStatic:
            self.runtimeDependencies["libs/openssl"] = None
            self.runtimeDependencies["libs/brotli"] = None
            self.runtimeDependencies["libs/zlib"] = None
            self.runtimeDependencies["libs/libzstd"] = None
            self.runtimeDependencies["libs/libpng"] = None
            self.runtimeDependencies["libs/libb2"] = None
            self.runtimeDependencies["libs/libjpeg-turbo"] = None
            self.runtimeDependencies["libs/sqlite"] = None
            self.runtimeDependencies["libs/freetype"] = None

            if self.options.dynamic.withDBus:
                self.runtimeDependencies["libs/dbus"] = None

            if self.options.dynamic.withICU:
                self.runtimeDependencies["libs/icu"] = None

            if self.options.dynamic.withHarfBuzz:
                self.runtimeDependencies["libs/harfbuzz"] = None

            if self.options.dynamic.withFontConfig:
                self.runtimeDependencies["libs/fontconfig"] = None

            if CraftCore.compiler.isUnix and self.options.dynamic.withGlib:
                self.runtimeDependencies["libs/glib"] = None

            if self.options.dynamic.withPCRE2:
                self.runtimeDependencies["libs/pcre2"] = None

            if self.options.dynamic.withCUPS:
                self.runtimeDependencies["libs/cups"] = None


class Package(CraftPackageObject.get("libs/qt6").pattern):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.subinfo.options.configure.args += [
            # sometimes qt fails to pic up the basic things
            f"-DCMAKE_CXX_STANDARD_INCLUDE_DIRECTORIES={CraftCore.standardDirs.craftRoot()}/include",
            "-DFEATURE_pkg_config=ON",
            "-DFEATURE_system_sqlite=ON",
            "-DFEATURE_system_zlib=ON",
            f"-DFEATURE_system_libb2={self.subinfo.options.isActive('libs/libb2').asOnOff}",
            f"-DFEATURE_system_freetype={self.subinfo.options.isActive('libs/freetype').asOnOff}",
            f"-DFEATURE_system_jpeg={self.subinfo.options.isActive('libs/libjpeg-turbo').asOnOff}",
            "-DQT_FEATURE_sql_odbc=OFF",
            "-DFEATURE_openssl_linked=ON",
            "-DQT_BUILD_EXAMPLES=OFF",
            f"-DFEATURE_system_pcre2={self.subinfo.options.dynamic.withPCRE2.asOnOff}",
            f"-DFEATURE_system_harfbuzz={self.subinfo.options.dynamic.withHarfBuzz.asOnOff}",
            f"-DFEATURE_icu={self.subinfo.options.dynamic.withICU.asOnOff}",
            f"-DFEATURE_dbus={self.subinfo.options.dynamic.withDBus.asOnOff}",
            "-DFEATURE_dbus_linked=OFF",
            f"-DFEATURE_glib={self.subinfo.options.dynamic.withGlib.asOnOff}",
            f"-DFEATURE_fontconfig={self.subinfo.options.dynamic.withFontConfig.asOnOff}",
            f"-DCMAKE_INTERPROCEDURAL_OPTIMIZATION={self.subinfo.options.dynamic.useLtcg.asOnOff}",
        ]
        if CraftCore.compiler.isLinux:
            self.subinfo.options.configure.args += [
                f"-DFEATURE_cups={self.subinfo.options.dynamic.withCUPS.asOnOff}",
                "-DFEATURE_xcb=ON",
                f"-DQT_FEATURE_egl={self.subinfo.options.dynamic.withEgl.asOnOff}",
            ]

        if CraftCore.compiler.isAndroid:
            self.subinfo.options.configure.args += [f"-DANDROID_ABI={CraftCore.compiler.androidAbi}", "-DECM_THREADS_WORKAROUND=OFF"]
        elif CraftCore.compiler.isMacOS:
            self.subinfo.options.configure.args += ["-DQT_NO_HANDLE_APPLE_SINGLE_ARCH_CROSS_COMPILING=ON"]

    def configure(self):
        if CraftCore.compiler.isAndroid:
            env = {}
            env["ECM_THREADS_WORKAROUND"] = "OFF"
            with utils.ScopedEnv(env):
                return super().configure()
        else:
            return super().configure()
