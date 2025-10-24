import info
from Package.CMakePackageBase import CMakePackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["0.2.2"]:
            self.targets[ver] = f"https://github.com/libsndfile/libsamplerate/archive/{ver}.tar.gz"
            self.targetInstSrc[ver] = f"libsamplerate-{ver}"
        self.targetDigests["0.2.2"] = (["16e881487f184250deb4fcb60432d7556ab12cb58caea71ef23960aec6c0405a"], CraftHash.HashAlgorithm.SHA256)
        # cmake 4, based on 15c392d47e71b9395a759544b3818a1235fe1a1d.patch
        self.patchToApply["0.2.2"] = [("libsamplerate-0.2.2-20251024.diff", 1)]
        self.description = "an audio sample rate converter library"
        self.defaultTarget = "0.2.2"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None


class Package(CMakePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subinfo.options.configure.args += ["-DLIBSAMPLERATE_EXAMPLES=OFF"]
