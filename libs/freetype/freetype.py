import info
from CraftCore import CraftCore
from Package.AutoToolsPackageBase import AutoToolsPackageBase
from Package.CMakePackageBase import CMakePackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["2.12.1"]:
            self.targets[ver] = "https://downloads.sourceforge.net/freetype/freetype-" + ver + ".tar.xz"
            self.targetInstSrc[ver] = "freetype-" + ver
        self.targetDigests["2.12.1"] = (["4766f20157cc4cf0cd292f80bf917f92d1c439b243ac3018debf6b9140c41a7f"], CraftHash.HashAlgorithm.SHA256)
        self.defaultTarget = "2.12.1"
        self.description = "A Free, High-Quality, and Portable Font Engine"

        self.patchToApply["2.12.1"] = [("freetype-no-zlib-pkgconfig-android.patch", 1)]
        self.patchLevel["2.12.1"] = 3

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/libpng"] = None
        self.runtimeDependencies["libs/libbzip2"] = None
        self.runtimeDependencies["libs/zlib"] = None
        self.runtimeDependencies["libs/brotli"] = None
        self.buildDependencies["dev-utils/msys"] = None
        self.buildDependencies["dev-utils/pkg-config"] = None


class PackageCMake(CMakePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subinfo.options.configure.args += ["-DCMAKE_DISABLE_FIND_PACKAGE_HarfBuzz=TRUE", "-DDISABLE_FORCE_DEBUG_POSTFIX=ON", "-DFT_REQUIRE_BROTLI=ON"]


class PackageMSys(AutoToolsPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subinfo.options.configure.autoreconf = False
        self.subinfo.options.configure.args += ["--disable-static", "--enable-shared", "--with-harfbuzz=off", "--with-brotli=on"]


if CraftCore.compiler.isGCCLike() and CraftCore.compiler.platform.isAndroid:

    class Package(PackageMSys):
        pass

else:

    class Package(PackageCMake):
        pass
