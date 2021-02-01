import info


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["1.9.1"]:
            self.targets[ver] = f"http://doxygen.nl/files/doxygen-{ver}.windows.x64.bin.zip"
            self.targetInstallPath[ver] = "dev-utils/bin"

        self.targetDigests["1.9.1"] =  (['deb8e6e5f21c965ec07fd32589d0332eff047f2c8658b5c56be4839a5dd43353'], CraftHash.HashAlgorithm.SHA256)
        self.description = 'Automated C, C++, and Java Documentation Generator'
        self.defaultTarget = '1.9.1'


from Package.BinaryPackageBase import *


class Package(BinaryPackageBase):
    def __init__(self):
        BinaryPackageBase.__init__(self)
