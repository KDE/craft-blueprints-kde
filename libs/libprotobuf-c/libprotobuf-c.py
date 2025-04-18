import info
from Package.AutoToolsPackageBase import AutoToolsPackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets["master"] = "https://github.com/protobuf-c/protobuf-c.git"
        for ver in ["1.5.2"]:
            self.targets[ver] = f"https://github.com/protobuf-c/protobuf-c/archive/refs/tags/v{ver}.tar.gz"
            self.archiveNames[ver] = f"libprotobuf-c-{ver}.tar.gz"
            self.targetInstSrc[ver] = f"libprotobuf-c-{ver}"
        self.targetDigests["1.5.2"] = (["cea46eeaa19c52924938b582c5d128a6ed3b6fb5b3f4677476a1781cc06e03f3"], CraftHash.HashAlgorithm.SHA256)
        self.defaultTarget = "1.5.2"


class Package(AutoToolsPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subinfo.options.configure.args += [
            "-D--disable-protoc",
        ]
