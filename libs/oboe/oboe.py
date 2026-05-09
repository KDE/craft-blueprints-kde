import info
import utils
from CraftCore import CraftCore
from Package.CMakePackageBase import CMakePackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def setTargets(self):
        self.parent.package.categoryInfo.platforms = CraftCore.compiler.Platforms.Android
        self.defaultTarget = "1.9.3"
        self.targets[self.defaultTarget] = f"https://github.com/google/oboe/archive/refs/tags/{self.defaultTarget}.tar.gz"
        self.targetInstSrc[self.defaultTarget] = f"oboe-{self.defaultTarget}"
        self.targetDigests[self.defaultTarget] = (["9d2486b74bd396d9d9112625077d5eb656fd6942392dc25ebf222b184ff4eb61"], CraftHash.HashAlgorithm.SHA256)

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None


class Package(CMakePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subinfo.options.configure.args += ["-DBUILD_SHARED_LIBS=ON"]

    def install(self):
        if not super().install():
            return False

        imageRoot = self.installDir()
        if CraftCore.compiler.isAndroid:
            installedLibs = sorted(imageRoot.glob(f"**/lib/{CraftCore.compiler.androidAbi}/liboboe*.so"))
            if not installedLibs:
                installedLibs = sorted(imageRoot.glob("**/liboboe*.so"))
            if not installedLibs:
                CraftCore.log.error(f"Could not find installed Oboe library below {imageRoot}")
                return False

            installedLib = installedLibs[0]
            prefixDir = installedLib.parents[2]
            libDir = prefixDir / "lib"
            if not utils.copyFile(installedLib, libDir / installedLib.name, linkOnly=False):
                return False
            if not utils.copyFile(installedLib, libDir / "liboboe.so", linkOnly=False):
                return False
        else:
            prefixDir = imageRoot
            libDir = prefixDir / "lib"

        pkgConfigDir = libDir / "pkgconfig"
        if not utils.createDir(pkgConfigDir):
            return False

        prefix = prefixDir
        if CraftCore.compiler.isAndroid:
            prefix = CraftCore.standardDirs.craftRoot()

        with open(pkgConfigDir / "oboe-1.0.pc", "wt", encoding="utf-8") as pcFile:
            pcFile.write(
                f"""prefix={prefix}
exec_prefix=${{prefix}}
libdir=${{prefix}}/lib
includedir=${{prefix}}/include

Name: oboe
Description: Oboe is a C++ library for high-performance audio apps on Android.
Version: {self.subinfo.buildTarget}
Libs: -L${{libdir}} -loboe -landroid -llog -lOpenSLES
Cflags: -I${{includedir}}
"""
            )

        return True
