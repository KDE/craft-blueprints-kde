import info


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["1.9.5"]:
            self.targets[ver] = f"https://doxygen.nl/files/doxygen-{ver}.windows.x64.bin.zip"
            self.targetInstallPath[ver] = "dev-utils/bin"

        self.targetDigests["1.9.5"] = (["8ae47b222d0cc0fb9bf001d5a01764cc478e0bf585492daa1003dfd836c72c25"], CraftHash.HashAlgorithm.SHA256)
        self.description = "Automated C, C++, and Java Documentation Generator"
        self.defaultTarget = "1.9.5"


from Package.BinaryPackageBase import *


class Package(BinaryPackageBase):
    def __init__(self):
        super().__init__()
