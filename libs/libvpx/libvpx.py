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

        for ver in ["1.16.0", "1.17.0"]:
            self.targets[ver] = f"https://github.com/webmproject/libvpx/archive/v{ver}.tar.gz"
            self.targetInstSrc[ver] = "libvpx-" + ver
        self.targetDigests["1.16.0"] = (["7a479a3c66b9f5d5542a4c6a1b7d3768a983b1e5c14c60a9396edc9b649e015c"], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests["1.17.0"] = (["1020f184046187baa2985dbde38e0691f49c44088bca7a1842b0236c6081dc0a"], CraftHash.HashAlgorithm.SHA256)

        self.patchToApply["1.16.0"] = [
            ("detect-clang.diff", 1),
            # ("mac.diff", 1),
            # https://github.com/microsoft/vcpkg/blob/b1a9ffcf749df96638bfebc8640e9c807cf45c0b/ports/libvpx/
            ("0006-gen-vcxproj-ignore-unknown-flags.patch", 1),
            ("0007-msvc-use-Fo-in-toolchain-probe.patch", 1),
            # Install the lib to lib/vpx.lib instead of lib/x64/vpxmd.lib
            ("adjust-msvc-lib-install-path.diff", 1),
        ]

        self.patchLevel["1.16.0"] = 1

        self.defaultTarget = "1.16.0"

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
        if CraftCore.compiler.isMSVC():
            self.platform = [
                f"--target={CraftCore.compiler.architecture.name.lower()}-win64-vs{CraftCore.compiler.getInternalVersion()}",
            ]
            self.subinfo.options.configure.args += ["--enable-external-build", "--as=nasm"]
        if CraftCore.compiler.isWindows:
            self.subinfo.options.configure.staticArgs = Arguments()
        self.subinfo.options.configure.args += [
            "--disable-examples",
            "--disable-install-docs",
            "--disable-unit-tests",
            "--disable-avx512",
            "--disable-docs",
            "--disable-tools",
        ]
