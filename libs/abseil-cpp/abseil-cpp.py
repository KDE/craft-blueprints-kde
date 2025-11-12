import info
from Package.CMakePackageBase import CMakePackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["20240116.2", "20250814.1"]:
            self.targets[ver] = f"https://github.com/abseil/abseil-cpp/releases/download/{ver}/abseil-cpp-{ver}.tar.gz"
            self.archiveNames[ver] = f"abseil-cpp-{ver}.tar.gz"
            self.targetInstSrc[ver] = f"abseil-cpp-{ver}"
        self.targetDigests["20240116.2"] = (["733726b8c3a6d39a4120d7e45ea8b41a434cdacde401cba500f14236c49b39dc"], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests["20250814.1"] = (["1692f77d1739bacf3f94337188b78583cf09bab7e420d2dc6c5605a4f86785a1"], CraftHash.HashAlgorithm.SHA256)

        # See https://github.com/abseil/abseil-cpp/issues/1717
        self.patchToApply["20240116.2"] = [("779a3565ac6c5b69dd1ab9183e500a27633117d5.patch", 1)]

        self.patchLevel["20240116.2"] = 4
        self.defaultTarget = "20250814.1"

        self.releaseManagerId = 115295
        self.webpage = "https://abseil.io/"
        self.description = "Abseil Common Libraries (C++)"

    def setDependencies(self):
        self.buildDependencies["virtual/base"] = None


class Package(CMakePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subinfo.options.configure.args += [
            "-DCMAKE_CXX_STANDARD=17",
            "-DABSL_PROPAGATE_CXX_STD=ON",
            "-DABSL_ENABLE_INSTALL=ON",
        ]
