import info

class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ['2.9']:
            self.targets[ver] = f"https://bitbucket.org/multicoreware/x265/downloads/x265_{ver}.tar.gz"
            self.targetInstSrc[ver] = f"x265_{ver}/source"
        self.targetDigests['2.9'] = (['ebae687c84a39f54b995417c52a2fdde65a4e2e7ebac5730d251471304b91024'], CraftHash.HashAlgorithm.SHA256)
        self.patchToApply['2.9'] = [('mingw-no-pdb.patch', 1)]
        self.description = "H.265/HEVC video stream encoder"
        self.defaultTarget = '2.9'

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.buildDependencies["dev-utils/nasm"] = None

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__(self, **args):
        CMakePackageBase.__init__(self)
        self.subinfo.options.configure.args = "-DEXPORT_C_API=ON -DENABLE_SHARED=ON -DENABLE_ASSEMBLY=ON -DENABLE_CLI=OFF"
