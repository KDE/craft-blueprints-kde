import info
from Package.MesonPackageBase import MesonPackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["2.12.0", "2.18.0", "2.20.0"]:
            self.targets[ver] = f"https://github.com/intel/libva/archive/refs/tags/{ver}.tar.gz"
            self.targetInstSrc[ver] = "libva-" + ver
        self.targetDigests["2.12.0"] = (["7bca8c8a854653e15e602f243e2452e84e4b454b26549bf80a932ab29d7d6b21"], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests["2.18.0"] = (["9d666c70c12dfefcdd27ae7dea771557f75e24961d0ed4cb050d96fb6136f438"], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests["2.20.0"] = (["117f8d658a5fc9ea406ca80a3eb4ae1d70b15a54807c9ed77199c812bed73b60"], CraftHash.HashAlgorithm.SHA256)
        self.description = "an implementation for VA-API (Video Acceleration API)"
        self.defaultTarget = "2.20.0"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.buildDependencies["python-modules/meson"] = None


class Package(MesonPackageBase):
    def __init__(self, **args):
        super().__init__()
