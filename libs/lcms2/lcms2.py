import info
import utils
from CraftCore import CraftCore
from Package.AutoToolsPackageBase import AutoToolsPackageBase
from Package.CMakePackageBase import CMakePackageBase


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["2.3", "2.4", "2.5", "2.7"]:
            self.targets[ver] = f"http://download.sourceforge.net/lcms/lcms2-{ver}.tar.gz"
            self.targetInstSrc[ver] = "lcms2-" + ver
        self.patchToApply["2.3"] = [("lcms2-2.3-20120302.diff", 1)]
        self.patchToApply["2.4"] = [("lcms2-2.4-20130124.diff", 1)]
        self.patchToApply["2.5"] = [("lcms2-2.4-20130124.diff", 1)]
        self.patchToApply["2.7"] = [("lcms2-2.7-20130124.diff", 1)]
        self.targetDigests["2.3"] = "67d5fabda2f5777ca8387766539b9c871d993133"
        self.targetDigests["2.4"] = "9944902864283af49e4e21a1ca456db4e04ea7c2"
        self.targetDigests["2.5"] = "bab3470471fc7756c5fbe71be9a3c7d677d2ee7b"
        self.targetDigests["2.7"] = "625f0d74bad4a0f6f917120fd992437d26f754d2"

        self.description = "A small-footprint, speed optimized color management engine"
        self.defaultTarget = "2.7"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None


if not CraftCore.compiler.isWindows:

    class Package(AutoToolsPackageBase):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)

        def configure(self):
            if CraftCore.compiler.isAndroid:
                env = {}
                env["LDFLAGS"] = "-lm"
                with utils.ScopedEnv(env):
                    return super().configure()
            else:
                return super().configure()

else:

    class Package(CMakePackageBase):
        def __init__(self, **kwargs):
            super().__init__(**kwargs)
            if self.subinfo.options.buildStatic:
                self.subinfo.options.configure.args += ["-DBUILD_STATIC=ON", "-DBUILD_TESTS=ON", "-DBUILD_UTILS=ON"]
            else:
                self.subinfo.options.configure.args += ["-DBUILD_STATIC=OFF", "-DBUILD_TESTS=OFF", "-DBUILD_UTILS=OFF"]
