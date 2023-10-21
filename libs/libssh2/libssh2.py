# -*- coding: utf-8 -*-
import info
from Package.AutoToolsPackageBase import AutoToolsPackageBase


class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets["master"] = "https://github.com/libssh2/libssh2.git"
        for ver in ["1.10.0", "1.11.0"]:
            self.targets[ver] = f"https://www.libssh2.org/download/libssh2-{ver}.tar.gz"
            self.targetInstSrc[ver] = f"libssh2-{ver}"
        self.targetDigests["1.10.0"] = (["2d64e90f3ded394b91d3a2e774ca203a4179f69aebee03003e5a6fa621e41d51"], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests["1.11.0"] = (["3736161e41e2693324deb38c26cfdc3efe6209d634ba4258db1cecff6a5ad461"], CraftHash.HashAlgorithm.SHA256)
        self.patchToApply["1.10.0"] = [("libssh2-1.10.0-20221026.diff", 1)]  # don't let pkg-config search for ws2_32
        if CraftCore.compiler.isMSVC():
            self.patchToApply["1.11.0"] = [("libssh2-1.11.0-MSVC-libprefix.pc.diff", 1)]
        self.patchLevel["1.10.0"] = 1
        self.defaultTarget = "1.11.0"

    def setDependencies(self):
        self.buildDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/zlib"] = None
        self.runtimeDependencies["libs/openssl"] = None


from Package.CMakePackageBase import *

if not CraftCore.compiler.isGCCLike():

    class Package(CMakePackageBase):
        def __init__(self, **args):
            CMakePackageBase.__init__(self)
            self.subinfo.options.dynamic.buildTests = False
            self.subinfo.options.dynamic.buildStatic = False
            self.subinfo.options.configure.args += ["-DENABLE_ZLIB_COMPRESSION=ON", "-DBUILD_EXAMPLES=OFF"]

else:

    class Package(AutoToolsPackageBase):
        def __init__(self, **args):
            AutoToolsPackageBase.__init__(self)
            # configure.ac:129: error: m4_undefine: undefined macro: backend
            self.subinfo.options.configure.autoreconf = False
            self.subinfo.options.configure.args += ["--disable-static", "--enable-shared"]
