import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets['master'] = "[git]https://github.com/lz4/lz4.git"
        for ver in ["1.9.2"]:
            self.targets[ver] = f"https://github.com/lz4/lz4/archive/v{ver}.tar.gz"
            self.targetInstSrc[ver] = f"lz4-{ver}"
            self.archiveNames[ver] = f"lz4-{ver}.tar.gz"
        self.targetDigests['1.9.2'] = (
            ['658ba6191fa44c92280d4aa2c271b0f4fbc0e34d249578dd05e50e76d0e5efcc'], CraftHash.HashAlgorithm.SHA256)
        self.description = 'Extremely Fast Compression algorithm'
        self.defaultTarget = '1.9.2'

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
