import info
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["8.45"]:
            self.targets[ver] = f"https://files.kde.org/craft/sources/libs/pcre/pcre-{ver}.tar.bz2"
            self.targetInstSrc[ver] = f"pcre-{ver}"
        self.patchToApply["8.45"] = [("pcre-8.10-20101125.diff", 1)]
        self.targetDigests["8.45"] = (["4dae6fdcd2bb0bb6c37b5f97c33c2be954da743985369cddac3546e3218bffb8"], CraftHash.HashAlgorithm.SHA256)

        self.description = "Perl-Compatible Regular Expressions"
        self.defaultTarget = "8.45"

    def setDependencies(self):
        self.buildDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/libbzip2"] = None
        self.runtimeDependencies["libs/zlib"] = None


class Package(CMakePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subinfo.options.dynamic.buildStatic = False

        self.subinfo.options.configure.args += ["-DPCRE_SUPPORT_UNICODE_PROPERTIES=ON", "-DPCRE_SUPPORT_UTF8=ON", "-DPCRE_EBCDIC=OFF"]
        if CraftCore.compiler.isAndroid:
            self.subinfo.options.configure.args += ["-DHAVE_STRTOQ=FALSE", "-DPCRE_BUILD_PCREGREP=FALSE", "-DPCRE_BUILD_TEST=FALSE"]
