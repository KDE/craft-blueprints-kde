import info

from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setTargets(self):
        self.targets['0.1.9'] = "http://www.mega-nerd.com/SRC/libsamplerate-0.1.9.tar.gz"
        self.targetInstSrc['0.1.9'] = 'libsamplerate-0.1.9'
        self.targetDigests['0.1.9'] = 'ed60f957a4ff87aa15cbb1f3dbd886fa7e5e9566'
        self.patchToApply['0.1.9'] = ('libsamplerate-0.1.9-20180928.diff', 1)
        self.description = "an audio sample rate converter library"
        self.defaultTarget = '0.1.9'

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = "default"
        self.runtimeDependencies["libs/libsndfile"] = "default"


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
        self.subinfo.options.configure.args = " -DBUILD_SHARED_LIB=ON -DBUILD_EXAMPLES=ON -DBUILD_TEST=ON"
