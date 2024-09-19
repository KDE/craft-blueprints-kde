import info
from CraftCore import CraftCore
from Package.CMakePackageBase import CMakePackageBase


class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets["master"] = "https://github.com/facebook/zstd.git"
        for ver in ["1.5.5", "1.5.6"]:
            self.targets[ver] = f"https://github.com/facebook/zstd/releases/download/v{ver}/zstd-{ver}.tar.gz"
            self.targetInstSrc[ver] = f"zstd-{ver}"
            self.targetConfigurePath[ver] = "build/cmake"
            self.targetDigestUrls[ver] = [f"https://github.com/facebook/zstd/releases/download/v{ver}/zstd-{ver}.tar.gz.sha256"]
        if CraftCore.compiler.isMSVC():
            self.patchToApply["1.5.6"] = [("3999.patch", 1)]
        self.description = "Fast real-time compression algorithm "
        self.defaultTarget = "1.5.6"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None


class Package(CMakePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subinfo.options.configure.args += [
            "-DZSTD_LEGACY_SUPPORT=ON",
            "-DZSTD_MULTITHREAD_SUPPORT=ON",
            "-DZSTD_BUILD_TESTS=OFF",
            "-DZSTD_BUILD_CONTRIB=OFF",
            f"-DZSTD_BUILD_PROGRAMS={self.subinfo.options.dynamic.buildTools.asOnOff}",
            f"-DZSTD_BUILD_STATIC={self.subinfo.options.dynamic.buildStatic.asOnOff}",
            f"-DZSTD_BUILD_SHARED={self.subinfo.options.dynamic.buildStatic.inverted.asOnOff}",
        ]
