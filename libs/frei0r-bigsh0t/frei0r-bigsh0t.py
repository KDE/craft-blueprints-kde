import info
from Package.CMakePackageBase import CMakePackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def setTargets(self):
        self.description = "frei0r plugins for VR video"

        for ver in ["2.6"]:
            self.targets[ver] = f"https://bitbucket.org/leo_sutic/bigsh0t/get/{ver}.tar.bz2"

        # 2.6
        self.targetDigests["2.6"] = (["001ed35ef06013a5a83b80c808194f3c5c2339c1759b52dda5bee523ce1f5517"], CraftHash.HashAlgorithm.SHA256)
        self.targetInstSrc["2.6"] = "leo_sutic-bigsh0t-d973312f2c1f"
        self.patchToApply["2.6"] = [("cmake-install-plugins-2.6.diff", 1)]
        self.patchLevel["2.6"] = 1

        self.defaultTarget = "2.6"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None


class Package(CMakePackageBase):
    def __init__(self, **args):
        super().__init__()
