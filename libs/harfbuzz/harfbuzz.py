import info
from Package.CMakePackageBase import CMakePackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["2.7.2"]:
            self.targets[ver] = f"https://github.com/harfbuzz/harfbuzz/archive/{ver}.tar.gz"
            self.targetInstSrc[ver] = "harfbuzz-" + ver
        self.targetDigests["2.7.2"] = (["8ec112ee108642477478b75fc7906422abed404d7530e47ba0a4875f553f1b59"], CraftHash.HashAlgorithm.SHA256)
        self.patchToApply["2.7.2"] = [("cmake-generate-pkgconfig.patch", 0)]
        self.description = "Text shaping library"
        self.defaultTarget = "2.7.2"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None


class Package(CMakePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subinfo.options.dynamic.buildStatic = False
        self.subinfo.options.configure.args += ["-DCMAKE_CXX_FLAGS=-DHB_NO_PRAGMA_GCC_DIAGNOSTIC_ERROR=1"]
