import info

from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setTargets(self):
        self.targets['0.1.7'] = "http://www.mega-nerd.com/SRC/libsamplerate-0.1.7.tar.gz"
        self.targetInstSrc['0.1.7'] = 'libsamplerate-0.1.7'
        self.targetDigests['0.1.7'] = 'f3f803ec5feae5a3fdb0fa3937277669e854386e'
        self.patchToApply['0.1.7'] = ('libsamplerate-0.1.7-20091002.diff', 1)
        self.description = "an audio sample rate converter library"
        self.defaultTarget = '0.1.7'

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = "default"
        self.runtimeDependencies["libs/libsndfile"] = "default"


class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
        self.subinfo.options.configure.args = " -DBUILD_SHARED_LIB=ON -DBUILD_EXAMPLES=ON -DBUILD_TESTS=ON"
