import info
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["1.4.4", "1.2.43", "1.5.14", "1.5.28", "1.6.6", "1.6.27", "1.6.37", "1.6.39"]:
            self.targets[ver] = "http://downloads.sourceforge.net/libpng/libpng-" + ver + ".tar.gz"
            self.targetInstSrc[ver] = "libpng-" + ver

        self.patchToApply["1.6.37"] = [
            ("libpng-1.6.37-20190911.diff", 1),
            ("libpng-1.6.37-20201106.diff", 1),
            ("libpng-1.6.37-20201116.diff", 1),
            ("libpng-1.6.37-20201123.diff", 1),
            ("libpng-fix-android-shared-build.diff", 1),
        ]
        self.patchToApply["1.6.39"] = [("libpng-1.6.39-install.pc-on-windows.diff", 1), ("libpng-fix-android-shared-build.diff", 1)]
        self.targetDigests["1.4.4"] = "245490b22086a6aff8964b7d32383a17814d8ebf"
        self.targetDigests["1.5.14"] = "67f20d69564a4a50204cb924deab029f11ad2d3c"
        self.targetDigests["1.6.6"] = "609c355beef7c16ec85c4580eabd62efe75383af"
        self.targetDigests["1.5.28"] = (["7dd9931dbdd43865055eeba52778ace6df5712b7f6f80f73c2b16b912c124a87"], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests["1.6.27"] = (["c9d164ec247f426a525a7b89936694aefbc91fb7a50182b198898b8fc91174b4"], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests["1.6.37"] = (["daeb2620d829575513e35fecc83f0d3791a620b9b93d800b763542ece9390fb4"], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests["1.6.39"] = (["af4fb7f260f839919e5958e5ab01a275d4fe436d45442a36ee62f73e5beb75ba"], CraftHash.HashAlgorithm.SHA256)

        self.patchLevel["1.6.37"] = 3
        self.description = "A library to display png images"
        self.defaultTarget = "1.6.39"

    def setDependencies(self):
        self.runtimeDependencies["libs/zlib"] = None
        self.runtimeDependencies["virtual/base"] = None


class Package(CMakePackageBase):
    def __init__(self, **args):
        CMakePackageBase.__init__(self)
        self.supportsCCACHE = False
        self.subinfo.options.configure.args += ["-DPNG_TESTS=OFF", "-DPNG_STATIC=OFF", "-DPNG_NO_STDIO=OFF"]
        if CraftCore.compiler.isMacOS:
            self.subinfo.options.configure.args += "-DPNG_ARM_NEON=off"
