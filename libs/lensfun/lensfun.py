import info
from CraftCompiler import CraftCompiler
from CraftCore import CraftCore
from Package.CMakePackageBase import CMakePackageBase
from Utils import CraftHash
from Utils.CraftBool import CraftBool


class subinfo(info.infoclass):
    def registerOptions(self):
        self.options.dynamic.setDefault("buildTests", self.options.dynamic.buildTests and not CraftCore.compiler.isWindows)

    def setTargets(self):
        for ver in ["0.2.6", "0.3.2", "0.3.95"]:
            self.targets[ver] = f"https://github.com/lensfun/lensfun/archive/v{ver}.tar.gz"
            self.targetInstSrc[ver] = f"lensfun-{ver}"

        self.targetDigests["0.2.6"] = "ed20d5a04ff5785d15ea8e135bc125752d2d5a73"
        self.targetDigests["0.3.2"] = "1d978b15aa7304d66a4931fa37ca9f8f89396c16"
        self.targetDigests["0.3.95"] = (["82c29c833c1604c48ca3ab8a35e86b7189b8effac1b1476095c0529afb702808"], CraftHash.HashAlgorithm.SHA256)

        self.patchToApply["0.2.6"] = ("lensfun-0.2.6.diff", 1)
        self.patchToApply["0.3.2"] = [("lensfun-0.3.2.patch", 1), ("lensfun-0.3.2-20200226.diff", 1), ("lensfun-0.3.2-20210816.diff", 1)]
        self.patchToApply["0.3.95"] = [("lensfun-0.3.95-20251112.diff", 1)]

        self.defaultTarget = "0.3.95"

        self.releaseManagerId = 1548
        self.webpage = "https://lensfun.github.io/"
        self.description = "a library to perform image correction based on lens profiles"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        # self.buildDependencies["dev-utils/doxygen"] = None
        self.runtimeDependencies["libs/glib"] = None
        # self.runtimeDependencies['libs-bin/zlib'] = None # only needed if building auxfun and tests
        # self.runtimeDependencies['libs-bin/libpng'] = None # only needed if building auxfun and tests


class Package(CMakePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        disableSSE = CraftBool(CraftCore.compiler.isMacOS and CraftCore.compiler.architecture == CraftCompiler.Architecture.arm64)

        self.subinfo.options.configure.args = [
            "-DCMAKE_POLICY_VERSION_MINIMUM=3.5",
            f"-DBUILD_STATIC={self.subinfo.options.dynamic.buildStatic.asOnOff}",
            f"-DBUILD_TESTS={self.subinfo.options.dynamic.buildTests.asOnOff}",
            "-DBUILD_AUXFUN=OFF",
            f"-DBUILD_FOR_SSE={disableSSE.inverted.asOnOff}",
            f"-DBUILD_FOR_SSE2={disableSSE.inverted.asOnOff}",
            "-DBUILD_DOC=OFF",
        ]
