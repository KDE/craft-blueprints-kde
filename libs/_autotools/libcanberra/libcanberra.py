import info


class subinfo(info.infoclass):
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


from Package.AutoToolsPackageBase import *


class Package(AutoToolsPackageBase):
    def __init__(self, **args):
        AutoToolsPackageBase.__init__(self)
