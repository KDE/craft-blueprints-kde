import info
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ['10.35']:
            self.targets[ver] = f"https://ftp.pcre.org/pub/pcre/pcre2-{ver}.tar.gz"
            self.targetInstSrc[ver] = 'pcre2-' + ver

        self.patchToApply["10.35"] = [("pcre2-10.35-20201102.diff", 1), ("pcre2-10.35-20201106.diff", 1)]
        self.targetDigests["10.35"] = (['8fdcef8c8f4cd735169dd0225fd010487970c1bcadd49e9b90e26c7250a33dc9'], CraftHash.HashAlgorithm.SHA256)
        self.patchLevel["10.35"] = 2

        self.description = "Perl-Compatible Regular Expressions (version2)"
        self.defaultTarget = '10.35'

    def setDependencies(self):
        self.buildDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/libbzip2"] = None
        self.runtimeDependencies["libs/zlib"] = None


class Package(CMakePackageBase):
    def __init__(self, **args):
        CMakePackageBase.__init__(self)
        self.subinfo.options.configure.args += " -DBUILD_SHARED_LIBS=ON -DPCRE2_BUILD_PCRE2_16=ON -DPCRE2_BUILD_PCRE2_32=ON"
