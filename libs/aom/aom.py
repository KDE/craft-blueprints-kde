import info
from Package.CMakePackageBase import *

class subinfo(info.infoclass):
    def setTargets(self):
        self.description = "An open, royalty-free video coding format designed for video transmissions over the Internet"
        ver = "3.1.3"
        self.defaultTarget = ver
        self.targets[ver] = f"https://aomedia.googlesource.com/aom.git/+archive/v{ver}.tar.gz"
        self.targetDigests[ver] =  (['b524316c7e32f79ea66f1c059908fa86297906c6e161e8c7cc4ca65a13cbc8ae'], CraftHash.HashAlgorithm.SHA256)

    def setDependencies(self):
        self.buildDependencies["dev-utils/cmake"] = None
        self.buildDependencies["dev-utils/perl"] = None
        self.buildDependencies["dev-utils/yasm"] = None
        self.runtimeDependencies["virtual/base"] = None


class Package(CMakePackageBase):
    def __init__(self, **args):
        CMakePackageBase.__init__(self)
        self.subinfo.options.configure.args += " -DBUILD_SHARED_LIBS=ON"
