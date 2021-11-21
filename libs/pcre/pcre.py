import info
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["8.45", "8.41"]:
            self.targets[ver] = f"https://download.sourceforge.net/pcre/pcre-{ver}.tar.bz2"
            self.targetInstSrc[ver] = f"pcre-{ver}"
        self.patchToApply["8.41"] = [("pcre-8.10-20101125.diff", 1)]
        self.patchToApply["8.45"] = [("pcre-8.10-20101125.diff", 1)]
        self.targetDigests['8.41'] = (
            ['e62c7eac5ae7c0e7286db61ff82912e1c0b7a0c13706616e94a7dd729321b530'], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests['8.45'] = (
            ['4dae6fdcd2bb0bb6c37b5f97c33c2be954da743985369cddac3546e3218bffb8'], CraftHash.HashAlgorithm.SHA256)

        self.description = "Perl-Compatible Regular Expressions"
        if CraftCore.compiler.isAndroid:
            self.defaultTarget = "8.45"
        else:
            self.defaultTarget = "8.41"

    def setDependencies(self):
        self.buildDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/libbzip2"] = None
        self.runtimeDependencies["libs/zlib"] = None


class Package(CMakePackageBase):
    def __init__(self, **args):
        CMakePackageBase.__init__(self)

        defines = "-DBUILD_SHARED_LIBS=ON "
        defines += "-DPCRE_SUPPORT_UNICODE_PROPERTIES=ON "
        defines += "-DPCRE_SUPPORT_UTF8=ON "
        defines += "-DPCRE_EBCDIC=OFF "
        if CraftCore.compiler.isAndroid:
            defines += "-DHAVE_STRTOQ=FALSE -DPCRE_BUILD_PCREGREP=FALSE -DPCRE_BUILD_TEST=FALSE"
        self.subinfo.options.configure.args = defines
