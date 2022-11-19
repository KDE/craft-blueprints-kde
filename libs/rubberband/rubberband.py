import info

from Package.MSBuildPackageBase import *

class subinfo(info.infoclass):
    def registerOptions(self):
        self.parent.package.categoryInfo.platforms = CraftCore.compiler.Platforms.NotMacOS

    def setTargets( self ):
        for ver in ["3.1.1"]:
            self.targets[ver] = f"https://github.com/breakfastquay/rubberband/archive/v{ver}.tar.gz"
            self.targetInstSrc[ver] = f"rubberband-{ver}"
            self.patchToApply[ver] = ("fftw3-linking.patch", 0)
        self.targetDigests["3.1.1"] = (['5d55a7af87e50dd30e963b2b04edd4729decfdcbbe8d16346812a3cfeb7b5a2b'], CraftHash.HashAlgorithm.SHA256)
        self.description = "An audio time-stretching and pitch-shifting library and utility program"
        self.webpage = "http://breakfastquay.com/rubberband/"
        self.patchLevel["3.1.1"] = 1
        self.defaultTarget = "3.1.1"

    def setDependencies( self ):
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/libfftw"] = None
        self.runtimeDependencies["libs/libsamplerate"] = None
        self.runtimeDependencies["libs/libsndfile"] = None
        self.buildDependencies["python-modules/meson"] = None

from Package.MesonPackageBase import *

class Package(MesonPackageBase):
    def __init__(self, **args):
        MesonPackageBase.__init__(self)
