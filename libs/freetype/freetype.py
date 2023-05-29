import info
from Package.AutoToolsPackageBase import AutoToolsPackageBase
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["2.12.1"]:
            self.targets[ver] = "http://downloads.sourceforge.net/freetype/freetype-" + ver + ".tar.xz"
            self.targetInstSrc[ver] = "freetype-" + ver
        self.targetDigests["2.12.1"] = (["4766f20157cc4cf0cd292f80bf917f92d1c439b243ac3018debf6b9140c41a7f"], CraftHash.HashAlgorithm.SHA256)
        self.defaultTarget = "2.12.1"
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
        self.subinfo.options.configure.args += ["-DCMAKE_DISABLE_FIND_PACKAGE_HarfBuzz=TRUE", "-DDISABLE_FORCE_DEBUG_POSTFIX=ON", "-DFT_DISABLE_BROTLI=OFF"]


class PackageMSys(AutoToolsPackageBase):
    def __init__(self):
        AutoToolsPackageBase.__init__(self)
        self.subinfo.options.configure.autoreconf = False
        self.subinfo.options.configure.args += ["--disable-static", "--enable-shared", "--with-harfbuzz=off", "--with-brotli=off"]


if CraftCore.compiler.isGCCLike() and not CraftCore.compiler.isAndroid:

    class Package(PackageMSys):
        pass

else:

    class Package(PackageCMake):
        pass
