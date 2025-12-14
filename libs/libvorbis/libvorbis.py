import info
from Package.CMakePackageBase import CMakePackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["1.3.7"]:
            self.targets[ver] = f"https://downloads.xiph.org/releases/vorbis/libvorbis-{ver}.tar.gz"
            self.targetInstSrc[ver] = "libvorbis-" + ver
        self.targetDigests["1.3.7"] = (["0e982409a9c3fc82ee06e08205b1355e5c6aa4c36bca58146ef399621b0ce5ab"], CraftHash.HashAlgorithm.SHA256)
        self.patchToApply["1.3.7"] = [
            ("0003-def-mingw-compat.patch", 1),
            ("update-minimum-cmake-version-to-3.6.patch", 1),
        ]
        self.patchLevel["1.3.7"] = 2

        self.description = "reference implementation for the vorbis audio file format"
        self.defaultTarget = "1.3.7"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/libogg"] = None


class Package(CMakePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subinfo.options.configure.args += ["-DCMAKE_MACOSX_RPATH=1"]
