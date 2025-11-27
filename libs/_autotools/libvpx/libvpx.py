import os

import info
from CraftCore import CraftCore
from Package.AutoToolsPackageBase import AutoToolsPackageBase
from Utils import CraftHash
from Utils.Arguments import Arguments


class subinfo(info.infoclass):
    def setTargets(self):
        self.description = "VP8 and VP9 video codec"
        self.releaseManagerId = 11083
        self.webpage = "https://www.webmproject.org/"

        for ver in ["1.15.2"]:
            self.targets[ver] = f"https://github.com/webmproject/libvpx/archive/v{ver}.tar.gz"
            self.targetInstSrc[ver] = "libvpx-" + ver
        self.targetDigests["1.15.2"] = (["26fcd3db88045dee380e581862a6ef106f49b74b6396ee95c2993a260b4636aa"], CraftHash.HashAlgorithm.SHA256)

        self.patchToApply["1.15.2"] = [("detect-clang.diff", 1), ("mac.diff", 1)]

        self.defaultTarget = "1.15.2"

    def setDependencies(self):
        self.buildDependencies["dev-utils/nasm"] = None


class Package(AutoToolsPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subinfo.options.configure.noDataRootDir = True
        self.subinfo.options.configure.noCacheFile = True
        self.platform = ""
        if CraftCore.compiler.isMacOS and not CraftCore.compiler.isNative():
            self.platform = [
                f"--target={CraftCore.compiler.architecture.name.lower()}-darwin{os.uname().release.split('.')[0]}-gcc",
            ]
        if CraftCore.compiler.isMinGW():
            self.subinfo.options.configure.staticArgs = Arguments()
        self.subinfo.options.configure.args += ["--disable-examples", "--disable-install-docs", "--disable-unit-tests", "--disable-avx512"]
