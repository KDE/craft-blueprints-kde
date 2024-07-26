import info


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["20240116.2"]:
            self.targets[ver] = f"https://github.com/abseil/abseil-cpp/releases/download/{ver}/abseil-cpp-{ver}.tar.gz"
            self.archiveNames[ver] = f"abseil-cpp-{ver}.tar.gz"
            self.targetInstSrc[ver] = f"abseil-cpp-{ver}"
        self.targetDigests["20240116.2"] = (["733726b8c3a6d39a4120d7e45ea8b41a434cdacde401cba500f14236c49b39dc"], CraftHash.HashAlgorithm.SHA256)
        self.patchLevel["20240116.2"] = 3
        self.defaultTarget = "20240116.2"

    def setDependencies(self):
        self.buildDependencies["virtual/base"] = None


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subinfo.options.configure.args += [
            "-DCMAKE_CXX_STANDARD=17",
            "-DABSL_PROPAGATE_CXX_STD=ON",
            "-DABSL_ENABLE_INSTALL=ON",
        ]
