import info
from Package.CMakePackageBase import CMakePackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def setTargets(self):
        self.description = "a library for dealing with Microsoft ITSS/CHM format files"

        for ver in ["0.40"]:
            # the server does not support https
            self.targets[ver] = f"https://files.kde.org/craft/sources/libs/chm/chmlib-{ver}.tar.bz2"
            self.targetInstSrc[ver] = f"chmlib-{ver}"
        self.patchToApply["0.40"] = ("chm-cmake.diff", 0)
        self.patchLevel["0.40"] = 1
        self.targetDigests["0.40"] = (["3449d64b0cf71578b2c7e3ddc048d4af3661f44a83941ea074a7813f3a59ffa3"], CraftHash.HashAlgorithm.SHA256)

        self.releaseManagerId = 17678
        self.webpage = "http://www.jedrea.com/chmlib/"

        self.defaultTarget = "0.40"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None


class Package(CMakePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # building examples and debugging tools
        self.subinfo.options.configure.args += ["-DCMAKE_POLICY_VERSION_MINIMUM=3.5", "-DBUILD_examples=OFF"]
