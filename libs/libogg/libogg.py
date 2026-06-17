import info
from Package.CMakePackageBase import CMakePackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["1.3.6"]:
            self.targets[ver] = f"https://downloads.xiph.org/releases/ogg/libogg-{ver}.tar.gz"
            self.targetInstSrc[ver] = "libogg-" + ver
        self.targetDigests["1.3.6"] = (["83e6704730683d004d20e21b8f7f55dcb3383cdf84c0daedf30bde175f774638"], CraftHash.HashAlgorithm.SHA256)

        self.description = "reference implementation for the ogg audio file format"
        self.defaultTarget = "1.3.6"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None


class Package(CMakePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subinfo.options.configure.args += ["-DINSTALL_DOCS=OFF"]
