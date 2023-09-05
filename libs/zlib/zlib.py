# -*- coding: utf-8 -*-
import info
from Package.AutoToolsPackageBase import AutoToolsPackageBase
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def registerOptions(self):
        self.parent.package.categoryInfo.platforms = CraftCore.compiler.Platforms.NotAndroid

    def setTargets(self):
        for ver in ["1.2.13"]:
            self.targets[ver] = f"https://github.com/madler/zlib/releases/download/v{ver}/zlib-{ver}.tar.xz"
            self.targetInstSrc[ver] = f"zlib-{ver}"
        self.patchToApply["1.2.13"] = [
            ("zlib-1.2.12-20220404.diff", 1),
            (
                # don't conditonlessly define Z_HAVE_UNISTD_H
                "zlib-1.2.12-20220503.diff",
                1,
            ),
        ]
        self.targetDigests["1.2.13"] = (
            ["d14c38e313afc35a9a8760dadf26042f51ea0f5d154b0630a31da0540107fb98"],
            CraftHash.HashAlgorithm.SHA256,
        )

        self.description = "The zlib compression and decompression library"
        self.webpage = "https://www.zlib.net"
        self.patchLevel["1.2.13"] = 1
        self.defaultTarget = "1.2.13"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None


if CraftCore.compiler.isWindows:

    class Package(CMakePackageBase):
        def __init__(self, **args):
            CMakePackageBase.__init__(self)
            self.subinfo.options.configure.args += [f"-DINSTALL_PKGCONFIG_DIR={CraftCore.standardDirs.craftRoot() / 'lib/pkgconfig'}"]

else:

    class Package(AutoToolsPackageBase):
        def __init__(self, **args):
            AutoToolsPackageBase.__init__(self)
            self.subinfo.options.configure.autoreconf = False
            self.supportsCCACHE = False
            self.platform = ""
