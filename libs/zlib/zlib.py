# -*- coding: utf-8 -*-
import info
from Package.AutoToolsPackageBase import AutoToolsPackageBase
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def registerOptions(self):
        self.parent.package.categoryInfo.platforms = CraftCore.compiler.Platforms.NotAndroid

    def setTargets(self):
        for ver in ['1.2.12']:
            self.targets[ver] = f"https://www.zlib.net/zlib-{ver}.tar.xz"
            self.targetInstSrc[ver] = f"zlib-{ver}"
        self.targetDigests['1.2.12'] = (['7db46b8d7726232a621befaab4a1c870f00a90805511c0e0090441dac57def18'], CraftHash.HashAlgorithm.SHA256)

        self.patchToApply['1.2.12'] = [("zlib-1.2.12-fix-CC-logic-in-configure.patch", 1), # https://gitweb.gentoo.org/repo/gentoo.git/tree/sys-libs/zlib/files
                                       ("zlib-1.2.12-20220503.diff", 1) # fix ffmpeg
                                      ]
        if CraftCore.compiler.isWindows:
            self.patchToApply['1.2.12'] += [("zlib-1.2.12-20220404.diff", 1)]

        self.description = 'The zlib compression and decompression library'
        self.patchLevel["1.2.12"] = 2
        self.defaultTarget = '1.2.12'

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None


if CraftCore.compiler.isWindows:
    class Package(CMakePackageBase):
        def __init__(self, **args):
            CMakePackageBase.__init__(self)
            self.subinfo.options.configure.args += [f"-DINSTALL_PKGCONFIG_DIR={CraftCore.standardDirs.craftRoot() / 'lib/pkgconfig'}"   ]
else:
    class Package(AutoToolsPackageBase):
        def __init__(self, **args):
            AutoToolsPackageBase.__init__(self)
            self.subinfo.options.configure.autoreconf = False
            self.supportsCCACHE = False
            self.platform = ""