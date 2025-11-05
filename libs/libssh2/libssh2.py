# -*- coding: utf-8 -*-
import info
from CraftCore import CraftCore
from Package.CMakePackageBase import CMakePackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets["master"] = "https://github.com/libssh2/libssh2.git"
        for ver in ["1.10.0", "1.11.0", "1.11.1"]:
            self.targets[ver] = f"https://www.libssh2.org/download/libssh2-{ver}.tar.gz"
            self.targetInstSrc[ver] = f"libssh2-{ver}"
        self.targetDigests["1.10.0"] = (["2d64e90f3ded394b91d3a2e774ca203a4179f69aebee03003e5a6fa621e41d51"], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests["1.11.0"] = (["3736161e41e2693324deb38c26cfdc3efe6209d634ba4258db1cecff6a5ad461"], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests["1.11.1"] = (["d9ec76cbe34db98eec3539fe2c899d26b0c837cb3eb466a56b0f109cabf658f7"], CraftHash.HashAlgorithm.SHA256)
        self.patchToApply["1.10.0"] = [("libssh2-1.10.0-20221026.diff", 1)]  # don't let pkg-config search for ws2_32
        if CraftCore.compiler.isMSVC():
            self.patchToApply["1.11.0"] = [("libssh2-1.11.0-MSVC-libprefix.pc.diff", 1)]
            self.patchToApply["1.11.1"] = [("libssh2-1.11.1-20251027.diff", 1)]
        self.patchLevel["1.10.0"] = 1
        self.webpage = "https://github.com/libssh2/libssh2"
        self.defaultTarget = "1.11.1"

    def setDependencies(self):
        self.buildDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/zlib"] = None
        self.runtimeDependencies["libs/openssl"] = None


class Package(CMakePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subinfo.options.configure.args += [
            "-DENABLE_ZLIB_COMPRESSION=ON",
            "-DBUILD_EXAMPLES=OFF",
            "-DCRYPTO_BACKEND=OpenSSL",
            f"-DBUILD_SHARED_LIBS={self.subinfo.options.dynamic.buildStatic.inverted.asOnOff}",
            f"-DBUILD_STATIC_LIBS={self.subinfo.options.dynamic.buildStatic.asOnOff}",
        ]
