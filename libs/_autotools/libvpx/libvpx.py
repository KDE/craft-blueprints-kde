import info
from CraftCore import CraftCore
from Package.AutoToolsPackageBase import AutoToolsPackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def setTargets(self):
        self.description = "VP8 and VP9 video codec"

        for ver in ["1.9.0", "1.13.1"]:
            self.targets[ver] = f"https://github.com/webmproject/libvpx/archive/v{ver}.tar.gz"
            self.targetInstSrc[ver] = "libvpx-" + ver
        self.targetDigests["1.9.0"] = (["d279c10e4b9316bf11a570ba16c3d55791e1ad6faa4404c67422eb631782c80a"], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests["1.13.1"] = (["00dae80465567272abd077f59355f95ac91d7809a2d3006f9ace2637dd429d14"], CraftHash.HashAlgorithm.SHA256)

        self.patchToApply["1.9.0"] = [("detect-clang.diff", 1)]
        if CraftCore.compiler.isFreeBSD:
            self.patchToApply["1.9.0"] += [("dont-check-for-diff.diff", 1)]
        self.patchToApply["1.13.1"] = [("detect-clang.diff", 1)]

        self.defaultTarget = "1.13.1"

    def setDependencies(self):
        self.buildDependencies["dev-utils/nasm"] = None


class Package(AutoToolsPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subinfo.options.configure.noDataRootDir = True
        self.subinfo.options.configure.noCacheFile = True
        self.platform = ""
        self.subinfo.options.configure.args += ["--disable-examples", "--disable-install-docs", "--disable-unit-tests", "--disable-avx512"]
        if CraftCore.compiler.isLinux or CraftCore.compiler.isFreeBSD:
            self.subinfo.options.configure.args += ["--enable-shared"]
