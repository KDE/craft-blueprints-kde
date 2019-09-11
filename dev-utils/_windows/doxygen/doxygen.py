import info


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["1.8.16"]:
            self.targets[ver] = f"http://doxygen.nl/files/doxygen-{ver}.windows.x64.bin.zip"
            self.targetInstallPath[ver] = "dev-utils/bin"

        self.targetDigests['1.8.14'] = (['e2d635a05fb0516311071cfcc41a3859fa22a912b484ed2c2ddec70248b75845'], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests['1.8.16'] = (['c84890ec003841c1ee6ff35dd3b17fdfd5ae4c2914d1c8df11dcc3719d294ac5'], CraftHash.HashAlgorithm.SHA256)

        self.description = 'Automated C, C++, and Java Documentation Generator'
        self.defaultTarget = '1.8.16'


from Package.BinaryPackageBase import *


class Package(BinaryPackageBase):
    def __init__(self):
        BinaryPackageBase.__init__(self)
