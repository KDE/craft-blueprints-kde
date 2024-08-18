import info
from CraftCore import CraftCore
from Package.CMakePackageBase import CMakePackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["10.37", "10.42", "10.44"]:
            self.targets[ver] = f"https://github.com/PCRE2Project/pcre2/releases/download/pcre2-{ver}/pcre2-{ver}.tar.gz"
            self.targetInstSrc[ver] = f"pcre2-{ver}"

        self.patchToApply["10.37"] = [("pcre2-10.37-20211120.diff", 1)]
        self.targetDigests["10.37"] = (["04e214c0c40a97b8a5c2b4ae88a3aa8a93e6f2e45c6b3534ddac351f26548577"], CraftHash.HashAlgorithm.SHA256)
        self.patchLevel["10.37"] = 2
        self.targetDigests["10.42"] = (["c33b418e3b936ee3153de2c61cc638e7e4fe3156022a5c77d0711bcbb9d64f1f"], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests["10.44"] = (["86b9cb0aa3bcb7994faa88018292bc704cdbb708e785f7c74352ff6ea7d3175b"], CraftHash.HashAlgorithm.SHA256)

        self.description = "Perl-Compatible Regular Expressions (version2)"
        self.defaultTarget = "10.44"

    def setDependencies(self):
        self.buildDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/libbzip2"] = None
        self.runtimeDependencies["libs/zlib"] = None


class Package(CMakePackageBase):
    def __init__(self, **args):
        super().__init__(**args)
        self.subinfo.options.dynamic.buildStatic = False
        self.subinfo.options.configure.args += ["-DPCRE2_BUILD_PCRE2_16=ON", "-DPCRE2_BUILD_PCRE2_32=ON"]
        if CraftCore.compiler.isAndroid:
            self.subinfo.options.configure.args += ["-DPCRE2_BUILD_PCRE2GREP=OFF", "PCRE2_BUILD_TESTS=OFF"]
