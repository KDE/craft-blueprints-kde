import info
from CraftCore import CraftCore
from Package.MesonPackageBase import MesonPackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def registerOptions(self):
        self.parent.package.categoryInfo.platforms = CraftCore.compiler.Platforms.NotMacOS

    def setTargets(self):
        for ver in ["3.1.1", "3.1.3"]:
            self.targets[ver] = f"https://github.com/breakfastquay/rubberband/archive/v{ver}.tar.gz"
            self.targetInstSrc[ver] = f"rubberband-{ver}"
            self.patchToApply[ver] = ("fftw3-linking.patch", 0)
        self.targetDigests["3.1.1"] = (["5d55a7af87e50dd30e963b2b04edd4729decfdcbbe8d16346812a3cfeb7b5a2b"], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests["3.1.3"] = (["85f7fde23383a94c38955c3bb3fc29f59d2c0a1cad4aa31da539a92a3b5621db"], CraftHash.HashAlgorithm.SHA256)
        self.description = "An audio time-stretching and pitch-shifting library and utility program"
        self.webpage = "https://breakfastquay.com/rubberband/"
        self.defaultTarget = "3.1.3"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/libfftw"] = None
        self.runtimeDependencies["libs/libsamplerate"] = None
        self.runtimeDependencies["libs/libsndfile"] = None
        self.buildDependencies["python-modules/meson"] = None


class Package(MesonPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
