import info
from CraftCore import CraftCore
from Package.AutoToolsPackageBase import AutoToolsPackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def registerOptions(self):
        self.parent.package.categoryInfo.platforms &= CraftCore.compiler.Platforms.Linux | CraftCore.compiler.Platforms.FreeBSD

    def setTargets(self):
        for ver in ["0.30"]:
            self.targets[ver] = f"http://0pointer.de/lennart/projects/libcanberra/libcanberra-{ver}.tar.xz"
            self.targetInstSrc[ver] = f"libcanberra-{ver}"
        self.targetDigests["0.30"] = (["c2b671e67e0c288a69fc33dc1b6f1b534d07882c2aceed37004bf48c601afa72"], CraftHash.HashAlgorithm.SHA256)

        self.description = "A simple abstract interface for playing event sounds. It implements the XDG Sound Theme and Naming Specifications for generating event sounds on free desktops"
        self.webpage = "https://0pointer.de/lennart/projects/libcanberra/"
        self.defaultTarget = "0.30"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/libvorbis"] = None


class Package(AutoToolsPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
