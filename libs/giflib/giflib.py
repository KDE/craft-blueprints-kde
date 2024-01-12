import info
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["5.2.1"]:
            self.targets[ver] = "https://downloads.sourceforge.net/sourceforge/giflib/giflib-" + ver + ".tar.gz"
            self.targetInstSrc[ver] = "giflib-" + ver
        self.targetDigests["5.2.1"] = (["31da5562f44c5f15d63340a09a4fd62b48c45620cd302f77a6d9acf0077879bd"], CraftHash.HashAlgorithm.SHA256)
        # patches are from https://github.com/microsoft/vcpkg/tree/master/ports/giflib
        self.patchToApply["5.2.1"] = [("disable-GifDrawBoxedText8x8-win32.patch", 1), ("msvc-guard-unistd-h.patch", 1), ("giflib-5.2.1-20211120.diff", 1)]
        if CraftCore.compiler.isMSVC():
            self.patchToApply["5.2.1"] += [("fix-compile-error.patch", 1)]

        self.description = "GIF file manipulation library (utilities and docs)"
        self.defaultTarget = "5.2.1"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/zlib"] = None


class Package(CMakePackageBase):
    def __init__(self, **args):
        super().__init__()
        self.subinfo.options.configure.args += ["-DBUILD_utils=OFF", f"-DGIFLIB_EXPORTS={self.blueprintDir()}/exports.def"]
