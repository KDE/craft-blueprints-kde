import info
import utils
from CraftCore import CraftCore
from Package.AutoToolsPackageBase import AutoToolsPackageBase
from Package.MakeFilePackageBase import MakeFilePackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def registerOptions(self):
        # cyrus-sasl on MinGW does not work out of the box. It needs someone who cares
        self.parent.package.categoryInfo.platforms = (
            CraftCore.compiler.Compiler.NoCompiler if CraftCore.compiler.isMinGW() else CraftCore.compiler.Platforms.All
        )

    def setTargets(self):
        self.description = "Cyrus SASL implementation"

        for ver in ["2.1.28"]:
            self.targets[ver] = f"https://github.com/cyrusimap/cyrus-sasl/releases/download/cyrus-sasl-{ver}/cyrus-sasl-{ver}.tar.gz"
            self.targetInstSrc[ver] = f"cyrus-sasl-{ver}"

        # Backport https://github.com/cyrusimap/cyrus-sasl/pull/709 which is an error, not warning for us
        self.patchToApply["2.1.28"] = [("266f0acf7f5e029afbb3e263437039e50cd6c262.patch", 1)]
        self.targetDigests["2.1.28"] = (["7ccfc6abd01ed67c1a0924b353e526f1b766b21f42d4562ee635a8ebfc5bb38c"], CraftHash.HashAlgorithm.SHA256)

        self.patchLevel["2.1.28"] = 1

        self.defaultTarget = "2.1.28"
        self.webpage = "https://github.com/cyrusimap/cyrus-sasl"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/openssl"] = None
        self.runtimeDependencies["libs/lmdb"] = None


if CraftCore.compiler.isGCCLike():

    class Package(AutoToolsPackageBase):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            self.subinfo.options.configure.args += [
                "--disable-macos-framework",
                "--enable-sample=no",
                "--without-sqlite",
                "--with-openssl",
                "--without-pwcheck",
                "--without-authdaemond",
                "--with-dblib=lmdb",
            ]
            if CraftCore.compiler.isMinGW():
                self.subinfo.options.configure.args += ["--without-saslauthd"]

        def configure(self):
            if CraftCore.compiler.isMinGW():
                if not utils.copyFile(self.sourceDir() / "win32/include/md5global.h", self.sourceDir() / "include/md5global.h"):
                    return False
            return super().configure()

else:

    class Package(MakeFilePackageBase):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            # based on https://github.com/microsoft/vcpkg/blob/master/ports/cyrus-sasl/portfile.cmake
            self.subinfo.options.useShadowBuild = False
            self.subinfo.options.make.supportsMultijob = False
            self.subinfo.options.make.args += [
                "-f",
                self.sourceDir() / "NTMakefile",
                "CFG=Release",
                f"prefix={self.installDir()}",
                f"OPENSSL_LIBPATH={CraftCore.standardDirs.craftRoot()}\\lib",
                f"OPENSSL_INCLUDE={CraftCore.standardDirs.craftRoot()}\\include",
                "SASLDB=LMDB",
                f"LMDB_LIBPATH={CraftCore.standardDirs.craftRoot()}\\lib",
                "SUBDIRS=lib plugins utils",
                f"STATIC={self.subinfo.options.buildStatic.asOnOff.lower()}",
            ]
            self.subinfo.options.install.args += self.subinfo.options.make.args

        def configure(self):
            if not utils.copyFile(self.sourceDir() / "win32/include/md5global.h", self.sourceDir() / "include/md5global.h"):
                return False
            return super().configure()

        def install(self):
            if not super().install():
                return False
            pcFile = self.installDir() / "lib/pkgconfig/libsasl2.pc"
            if not utils.configureFile(
                self.sourceDir() / "libsasl2.pc.in",
                pcFile,
                {
                    "prefix": self.installPrefix().as_posix(),
                    "exec_prefix": "${prefix}/bin",
                    "libdir": "${prefix}/lib",
                    "includedir": "${prefix}/include",
                    "VERSION": self.buildTarget,
                    "LIB_DOOR": "",
                    "SASL_DL_LIB": "",
                    "LIBS": "",
                },
                atOnly=True,
            ):
                return False

            with pcFile.open("rt") as f:
                content = f.read()
            with pcFile.open("wt") as f:
                f.write(content.replace(" -lsasl2", " -llibsasl"))
            return True
