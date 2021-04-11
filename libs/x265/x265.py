import info

class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ['2.9', '3.4']:
            self.targets[ver] = f"http://deb.debian.org/debian/pool/main/x/x265/x265_{ver}.orig.tar.gz"
            self.targetInstSrc[ver] = f"x265_{ver}/source"
        self.targetDigests['2.9'] = (['ebae687c84a39f54b995417c52a2fdde65a4e2e7ebac5730d251471304b91024'], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests['3.4'] = (['c2047f23a6b729e5c70280d23223cb61b57bfe4ad4e8f1471eeee2a61d148672'], CraftHash.HashAlgorithm.SHA256)
        self.patchToApply['2.9'] = [('mingw-no-pdb.patch', 1)]
        self.description = "H.265/HEVC video stream encoder"
        self.defaultTarget = '3.4'

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.buildDependencies["dev-utils/nasm"] = None

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__(self, **args):
        CMakePackageBase.__init__(self)
        self.subinfo.options.configure.args = "-DEXPORT_C_API=ON -DENABLE_SHARED=ON -DENABLE_ASSEMBLY=ON -DENABLE_CLI=OFF"
