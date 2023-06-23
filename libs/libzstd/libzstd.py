import info
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets["master"] = "https://github.com/facebook/zstd.git"
        for ver in ["1.5.0", "1.5.2", "1.5.5"]:
            self.targets[ver] = f"https://github.com/facebook/zstd/releases/download/v{ver}/zstd-{ver}.tar.gz"
            self.targetInstSrc[ver] = f"zstd-{ver}"
            self.targetConfigurePath[ver] = "build/cmake"
        self.patchToApply["1.5.0"] = [("libzstd-1.5.0-20211104.diff", 1)]  # install .pc
        self.patchToApply["1.5.2"] = [("libzstd-1.5.0-20211104.diff", 1)]  # install .pc
        self.targetDigests["1.5.0"] = (["5194fbfa781fcf45b98c5e849651aa7b3b0a008c6b72d4a0db760f3002291e94"], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests["1.5.2"] = (["7c42d56fac126929a6a85dbc73ff1db2411d04f104fae9bdea51305663a83fd0"], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests["1.5.5"] = (["9c4396cc829cfae319a6e2615202e82aad41372073482fce286fac78646d3ee4"], CraftHash.HashAlgorithm.SHA256)
        self.description = "Fast real-time compression algorithm "
        self.defaultTarget = "1.5.5"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None


class Package(CMakePackageBase):
    def __init__(self, **args):
        CMakePackageBase.__init__(self)
        self.subinfo.options.configure.args += [
            "-DZSTD_LEGACY_SUPPORT=ON",
            "-DZSTD_MULTITHREAD_SUPPORT=ON",
            "-DZSTD_BUILD_TESTS=OFF",
            "-DZSTD_BUILD_CONTRIB=OFF",
        ]
