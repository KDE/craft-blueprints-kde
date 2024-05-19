import info
from Package.MesonPackageBase import MesonPackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["0.9.2", "1.2.0", "1.3.0"]:
            self.targets[ver] = f"https://code.videolan.org/videolan/dav1d/-/archive/{ver}/dav1d-{ver}.tar.bz2"
            self.targetInstSrc[ver] = f"dav1d-{ver}"
        self.targetDigests["0.9.2"] = (["0d198c4fe63fe7f0395b1b17de75b21c8c4508cd3204996229355759efa30ef8"], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests["1.2.0"] = (["05cedc43127e00a86c68b8a49a5f68e2dc22b9baa10b1e12a5e3bc5b37876a6b"], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests["1.3.0"] = (["bde8db3d0583a4f3733bb5a4ac525556ffd03ab7dcd8a6e7c091bee28d9466b1"], CraftHash.HashAlgorithm.SHA256)
        self.description = "dav1d is the fastest AV1 decoder on all platforms"
        self.defaultTarget = "1.3.0"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.buildDependencies["python-modules/meson"] = None
        self.buildDependencies["dev-utils/nasm"] = None


class Package(MesonPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subinfo.options.configure.args += [
            "-Denable_tests=false",
            "-Denable_tools=false",
        ]
