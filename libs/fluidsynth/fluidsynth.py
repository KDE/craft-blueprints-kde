import info
from Package.CMakePackageBase import CMakePackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["2.1.6", "2.2.3", "2.3.5"]:
            self.targets[ver] = f"https://github.com/FluidSynth/fluidsynth/archive/v{ver}.tar.gz"
            self.targetInstSrc[ver] = f"fluidsynth-{ver}"
        self.targetDigests["2.1.6"] = (["328fc290b5358544d8dea573f81cb1e97806bdf49e8507db067621242f3f0b8a"], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests["2.2.3"] = (["b31807cb0f88e97f3096e2b378c9815a6acfdc20b0b14f97936d905b536965c4"], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests["2.3.5"] = (["f89e8e983ecfb4a5b4f5d8c2b9157ed18d15ed2e36246fa782f18abaea550e0d"], CraftHash.HashAlgorithm.SHA256)
        self.patchToApply["2.1.6"] = [("fluidsynth-2.1.6-20210129.diff", 1)]

        self.description = "FluidSynth is a real-time software synthesizer based on the SoundFont 2 specifications and has reached widespread distribution."
        self.webpage = "http://www.fluidsynth.org/"
        self.defaultTarget = "2.3.5"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.buildDependencies["dev-utils/pkg-config"] = None
        self.runtimeDependencies["libs/glib"] = None
        self.runtimeDependencies["libs/libsndfile"] = None


class Package(CMakePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # dbus support needs a small patch on Windows but I have no idea why you would want dbus here
        self.subinfo.options.configure.args += ["-DLIB_SUFFIX=''", "-Denable-dbus=OFF"]
