import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.description = "frei0r plugins for VR video"

        for ver in ["2.5.1", "2.6"]:
            self.targets[ver] = "http://bitbucket.org/leo_sutic/bigsh0t/get/%s.tar.bz2" % ver

        # 2.5.1
        self.targetDigests["2.5.1"] = (["8c6ade9e1bca5d820948db443009da6bbec876cac8e0e2a0c5de269c577a5c32"], CraftHash.HashAlgorithm.SHA256)
        self.targetInstSrc["2.5.1"] = "leo_sutic-bigsh0t-dd6b0f7f2977"
        self.patchToApply["2.5.1"] = [("cmake-install-plugins-2.5.patch", 1)]
        self.patchLevel["2.5.1"] = 1

        # 2.6
        self.targetDigests["2.6"] = (["001ed35ef06013a5a83b80c808194f3c5c2339c1759b52dda5bee523ce1f5517"], CraftHash.HashAlgorithm.SHA256)
        self.targetInstSrc["2.6"] = "leo_sutic-bigsh0t-d973312f2c1f"
        self.patchToApply["2.6"] = [("cmake-install-plugins-2.6.diff", 1)]

        self.defaultTarget = "2.6"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self, **args):
        super().__init__()
