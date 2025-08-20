import info
from Package.MesonPackageBase import MesonPackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["3.1.3", "4.0.0"]:
            self.targets[ver] = f"https://github.com/breakfastquay/rubberband/archive/v{ver}.tar.gz"
            self.targetInstSrc[ver] = f"rubberband-{ver}"
            self.patchToApply[ver] = ("fftw3-linking.patch", 0)
        self.targetDigests["4.0.0"] = (["24300f48a8014b7c863b573a9647e61b1b19b37875e2cdd92005e64c6424d266"], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests["3.1.3"] = (["85f7fde23383a94c38955c3bb3fc29f59d2c0a1cad4aa31da539a92a3b5621db"], CraftHash.HashAlgorithm.SHA256)
        self.description = "An audio time-stretching and pitch-shifting library and utility program"
        self.webpage = "https://breakfastquay.com/rubberband/"
        self.defaultTarget = "4.0.0"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/libfftw"] = None
        self.runtimeDependencies["libs/libsamplerate"] = None
        self.runtimeDependencies["libs/libsndfile"] = None
        self.buildDependencies["python-modules/meson"] = None


class Package(MesonPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
