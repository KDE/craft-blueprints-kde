from ctypes import util
import info


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

        dataDir = CraftCore.standardDirs.locations.data.relative_to(CraftCore.standardDirs.craftRoot())
        self.subinfo.options.configure.args += [
            #"-DINSTALL_PUBLICBINDIR=bin",
            "-DINSTALL_BINDIR=lib/qt6/bin",
            "-DINSTALL_LIBEXECDIR=lib/qt6",
            "-DINSTALL_ARCHDATADIR=lib/qt6",
            "-DINSTALL_INCLUDEDIR=include/qt6",
            "-DINSTALL_MKSPECSDIR=lib/qt6/mkspecs",
            f"-DINSTALL_DOCDIR=doc/qt6",
            f"-DINSTALL_DATADIR={dataDir}/qt6",

            "-DFEATURE_pkg_config=ON",
            
            "-DFEATURE_system_sqlite=ON",
            "-DFEATURE_system_pcre2=ON",
            "-DFEATURE_system_zlib=ON",
            "-DFEATURE_system_harfbuzz=ON",
            "-DFEATURE_system_freetype=ON",

            "-DQT_BUILD_EXAMPLES=OFF"
        ]

        if self.subinfo.options.dynamic.useLtcg:
            self.subinfo.options.configure.args += ["-DCMAKE_INTERPROCEDURAL_OPTIMIZATION=ON"]

    def make(self):
        env = {}
        if CraftCore.compiler.isWindows:
            env["PATH"] = f"{self.buildDir() / 'lib/qt6/bin'};{os.environ['PATH']}"
        with utils.ScopedEnv(env):
            return super().make()

    def install(self):
        if not super().install():
            return False
        if CraftCore.compiler.isWindows:
            # TODO: there must be a more elegant way
            dll = utils.filterDirectoryContent(self.installDir() / "lib/qt6/bin",
                                                    whitelist=lambda x, root: x.name.endswith(".dll") or x.name.endswith("6.exe"),
                                                    blacklist=lambda x, root: True)
            utils.createDir(self.installDir() / "bin")
            for d in dll:
                src = Path(d)
                if not utils.copyFile(src, self.installDir() / "bin" / src.name):
                    return False
                src = src.with_suffix(".pdb")
                if src.exists():
                    if not utils.copyFile(src, self.installDir() / "bin" / src.name):
                        return False
        return True
