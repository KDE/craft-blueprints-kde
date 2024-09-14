import info
from Package.AutoToolsPackageBase import AutoToolsPackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["2.1.11"]:
            self.targets[ver] = f"https://github.com/libevent/libevent/releases/download/release-{ver}-stable/libevent-{ver}-stable.tar.gz"
            self.targetInstSrc[ver] = f"libevent-{ver}-stable"
        self.targetDigests["2.1.11"] = (["a65bac6202ea8c5609fd5c7e480e6d25de467ea1917c08290c521752f147283d"], CraftHash.HashAlgorithm.SHA256)
        self.defaultTarget = "2.1.11"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None


class Package(AutoToolsPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
