import info
from Package.AutoToolsPackageBase import AutoToolsPackageBase
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ['2.3.12', '2.5.0.1', '2.9.1']:
            self.targets[ver] = "http://downloads.sourceforge.net/freetype/freetype-" + ver + ".tar.bz2"
            self.targetInstSrc[ver] = "freetype-" + ver
        self.patchToApply['2.3.12'] = ('freetype-2.3.12.diff', 1)
        self.patchToApply['2.5.0.1'] = ('freetype-2.5.0.1.diff', 1)
        self.patchToApply['2.9.1'] = [("freetype-2.9.1-20180925.diff", 1),
                                      ("freetype-2.9.1-20180926.diff", 1)# TODO: cleanup the shared build
                                      ]
        self.targetDigests['2.3.12'] = 'ebf0438429c0bedd310059326d91646c3c91016b'
        self.targetDigests['2.5.0.1'] = '4bbd8357b4b723e1ff38414a9eaf50bf99dacb84'
        self.targetDigests['2.9.1'] = (['db8d87ea720ea9d5edc5388fc7a0497bb11ba9fe972245e0f7f4c7e8b1e1e84d'], CraftHash.HashAlgorithm.SHA256)
        self.patchLevel['2.9.1'] = 2
        self.defaultTarget = '2.9.1'
        self.description = "A Free, High-Quality, and Portable Font Engine"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/libpng"] = None
        self.runtimeDependencies["libs/libbzip2"] = None
        self.runtimeDependencies["libs/zlib"] = None
        self.buildDependencies["dev-utils/msys"] = None
        self.buildDependencies["dev-utils/pkg-config"] = None

class PackageCMake(CMakePackageBase):
    def __init__(self, **args):
        CMakePackageBase.__init__(self)
        self.subinfo.options.configure.args += ["-DFT_WITH_HARFBUZZ=OFF"]


class PackageMSys(AutoToolsPackageBase):
    def __init__(self):
        AutoToolsPackageBase.__init__(self)
        self.subinfo.options.configure.autoreconf = False
        self.subinfo.options.configure.args += ["--disable-static", "--enable-shared", "--with-harfbuzz=off"]



if CraftCore.compiler.isGCCLike() and not CraftCore.compiler.isAndroid:
    class Package(PackageMSys):
        pass
else:
    class Package(PackageCMake):
        pass
