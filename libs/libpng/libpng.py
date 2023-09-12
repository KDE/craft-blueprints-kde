import info
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["1.6.39", "1.6.40"]:
            self.targets[ver] = "https://downloads.sourceforge.net/libpng/libpng-" + ver + ".tar.gz"
            self.targetInstSrc[ver] = "libpng-" + ver

        self.patchToApply["1.6.39"] = [("libpng-1.6.39-install.pc-on-windows.diff", 1), ("libpng-fix-android-shared-build.diff", 1)]
        self.patchToApply["1.6.40"] = [("libpng-1.6.40-install.pc-on-windows.diff", 1)]
        self.targetDigests["1.6.39"] = (["af4fb7f260f839919e5958e5ab01a275d4fe436d45442a36ee62f73e5beb75ba"], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests["1.6.40"] = (["8f720b363aa08683c9bf2a563236f45313af2c55d542b5481ae17dd8d183bb42"], CraftHash.HashAlgorithm.SHA256)

        self.patchLevel["1.6.39"] = 1
        self.description = "A library to display png images"
        self.defaultTarget = "1.6.40"

    def setDependencies(self):
        self.runtimeDependencies["libs/zlib"] = None
        self.runtimeDependencies["virtual/base"] = None


class Package(CMakePackageBase):
    def __init__(self, **args):
        CMakePackageBase.__init__(self)
        self.supportsCCACHE = False
        self.subinfo.options.configure.args += ["-DPNG_TESTS=OFF", "-DPNG_STATIC=OFF", "-DPNG_NO_STDIO=OFF"]
        if CraftCore.compiler.isMacOS and self.subinfo.buildTarget == "1.6.39":
            self.subinfo.options.configure.args += ["-DPNG_ARM_NEON=off"]
