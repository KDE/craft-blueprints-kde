import info
from Package.CMakePackageBase import CMakePackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["1.21.1", "1.24.3"]:
            self.targets[ver] = f"https://github.com/kcat/openal-soft/archive/refs/tags/{ver}.tar.gz"
            self.targetInstSrc[ver] = f"openal-soft-{ver}"
        self.targetDigests["1.21.1"] = (["8ac17e4e3b32c1af3d5508acfffb838640669b4274606b7892aa796ca9d7467f"], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests["1.24.3"] = (["7e1fecdeb45e7f78722b776c5cf30bd33934b961d7fd2a11e0494e064cc631ce"], CraftHash.HashAlgorithm.SHA256)
        self.defaultTarget = "1.24.3"

        self.releaseManagerId = 8172
        self.webpage = "https://www.openal-soft.org/"
        self.description = "a library for audio support"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.buildDependencies["libs/qt/qtbase"] = None


class Package(CMakePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subinfo.options.configure.args += ["-DALSOFT_EXAMPLES=OFF"]
