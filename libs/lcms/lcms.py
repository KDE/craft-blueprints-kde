import info
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setTargets(self):
        self.targets['1.19'] = "http://download.sourceforge.net/lcms/lcms-1.19.tar.gz"
        self.targetInstSrc['1.19'] = "lcms-1.19"
        self.patchToApply['1.19'] = ('lcms-1.19-20101212.diff', 1)
        self.targetDigests['1.19'] = 'd5b075ccffc0068015f74f78e4bc39138bcfe2d4'
        self.description = "A small-footprint, speed optimized color management engine"
        self.defaultTarget = '1.19'

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = "default"


class Package(CMakePackageBase):
    def __init__(self, **args):
        CMakePackageBase.__init__(self)
        # both examples and tests can be run here
        self.subinfo.options.configure.args = "-DBUILD_TESTS=OFF -DBUILD_SAMPLES=ON -DBUILD_TOOLS=OFF"
