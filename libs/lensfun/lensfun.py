import info
from CraftCompiler import CraftCompiler
from CraftCore import CraftCore
from Package.CMakePackageBase import CMakePackageBase


class subinfo(info.infoclass):
    def setTargets(self):
        self.defaultTarget = "0.3.2"
        self.description = "a library to perform image correction based on lens profiles"

        for ver in ["0.2.6", "0.3.2"]:
            self.targets[ver] = "https://github.com/lensfun/lensfun/archive/v%s.tar.gz" % (ver)
            self.targetInstSrc[ver] = "lensfun-%s" % ver

        self.targetDigests["0.2.6"] = "ed20d5a04ff5785d15ea8e135bc125752d2d5a73"
        self.targetDigests["0.3.2"] = "1d978b15aa7304d66a4931fa37ca9f8f89396c16"

        self.patchToApply["0.2.6"] = ("lensfun-0.2.6.diff", 1)
        self.patchToApply["0.3.2"] = [("lensfun-0.3.2.patch", 1), ("lensfun-0.3.2-20200226.diff", 1), ("lensfun-0.3.2-20210816.diff", 1)]

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        # self.buildDependencies["dev-utils/doxygen"] = None
        self.runtimeDependencies["libs/glib"] = None
        # self.runtimeDependencies['libs-bin/zlib'] = None # only needed if building auxfun and tests
        # self.runtimeDependencies['libs-bin/libpng'] = None # only needed if building auxfun and tests


class Package(CMakePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        disableSSE = CraftCore.compiler.isMacOS and CraftCore.compiler.architecture == CraftCompiler.Architecture.arm64

        self.subinfo.options.configure.args = [
            "-DBUILD_STATIC=OFF",
            "-DBUILD_TESTS=OFF",
            "-DBUILD_AUXFUN=OFF",
            f"-DBUILD_FOR_SSE={'OFF' if disableSSE else 'ON'}",
            f"-DBUILD_FOR_SSE2={'OFF' if disableSSE else 'ON'}",
            "-DBUILD_DOC=OFF",
        ]
