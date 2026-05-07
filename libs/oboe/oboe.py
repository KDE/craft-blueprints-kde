import info
from CraftCore import CraftCore
from Package.CMakePackageBase import CMakePackageBase
from Utils import CraftHash
import utils


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

        if CraftCore.compiler.isAndroid:
            libName = "liboboe.so"
            abiLibDir = self.installDir() / "lib" / CraftCore.compiler.androidAbi
            if not utils.copyFile(abiLibDir / libName, self.installDir() / "lib" / libName, linkOnly=False):
                return False

        pkgConfigDir = self.installDir() / "lib/pkgconfig"
        if not utils.createDir(pkgConfigDir):
            return False
        with open(pkgConfigDir / "oboe-1.0.pc", "wt", encoding="utf-8") as pcFile:
            pcFile.write(
                f"""prefix={self.installDir()}
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
