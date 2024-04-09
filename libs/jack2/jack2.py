import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.description = "JACK Audio Connection Kit"
        self.webpage = "https://jackaudio.org/"
        self.svnTargets["master"] = "https://github.com/jackaudio/jack2"
        self.targetInstSrc["master"] = "common"
        self.patchToApply["master"] = ("jack2-cmake.patch", 0)
        for ver in ["1.9.14"]:
            self.targets[ver] = f"https://github.com/jackaudio/jack2/archive/v{ver}.tar.gz"
            self.targetInstSrc[ver] = "jack2-" + ver + "/common"
            self.patchToApply[ver] = ("jack2-cmake.patch", 1)
        self.targetDigests["1.9.14"] = (["a20a32366780c0061fd58fbb5f09e514ea9b7ce6e53b080a44b11a558a83217c"], CraftHash.HashAlgorithm.SHA256)
        self.patchLevel["1.9.14"] = 1
        self.defaultTarget = "1.9.14"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/tre"] = None


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
