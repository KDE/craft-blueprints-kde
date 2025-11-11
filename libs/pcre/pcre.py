import info
from CraftCore import CraftCore
from Package.CMakePackageBase import CMakePackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def registerOptions(self):
        # this blueprint is deprecated and only used to provides a regex replacement for openldap
        self.parent.package.categoryInfo.platforms = CraftCore.compiler.Platforms.Windows

    def setTargets(self):
        for ver in ["8.45"]:
            self.targets[ver] = f"https://files.kde.org/craft/sources/libs/pcre/pcre-{ver}.tar.bz2"
            self.targetInstSrc[ver] = f"pcre-{ver}"
        self.patchToApply["8.45"] = [
            ("pcre-8.45_suppress_cmake_and_compiler_warnings-errors.patch", 1)
        ]  # https://github.com/microsoft/vcpkg/blob/8fbf295ab5283313932f65a597a2c1f09a73fafd/ports/pcre/pcre-8.45_suppress_cmake_and_compiler_warnings-errors.patch
        self.targetDigests["8.45"] = (["4dae6fdcd2bb0bb6c37b5f97c33c2be954da743985369cddac3546e3218bffb8"], CraftHash.HashAlgorithm.SHA256)

        self.description = "Perl-Compatible Regular Expressions"
        self.webpage = "https://www.pcre.org/"
        self.releaseManagerId = 2610
        self.defaultTarget = "8.45"

    def setDependencies(self):
        self.buildDependencies["virtual/base"] = None


class Package(CMakePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subinfo.options.configure.args += [
            "-DCMAKE_POLICY_VERSION_MINIMUM=3.5",
            "-DPCRE_SUPPORT_UNICODE_PROPERTIES=ON",
            "-DPCRE_SUPPORT_UTF8=ON",
            "-DPCRE_EBCDIC=OFF",
            "-DPCRE_BUILD_PCREGREP=OFF",
            "-DPCRE_BUILD_TESTS=OFF",
            "-DPCRE_SUPPORT_LIBBZ2=OFF",
            "-DPCRE_SUPPORT_LIBZ=OFF",
            "-DPCRE_SUPPORT_LIBEDIT=OFF",
            "-DPCRE_SUPPORT_LIBREADLINE=OFF",
        ]
