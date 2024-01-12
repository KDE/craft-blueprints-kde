import info


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["2.1.6", "2.2.3"]:
            self.targets[ver] = f"https://github.com/FluidSynth/fluidsynth/archive/v{ver}.tar.gz"
            self.targetInstSrc[ver] = f"fluidsynth-{ver}"
        self.targetDigests["2.1.6"] = (["328fc290b5358544d8dea573f81cb1e97806bdf49e8507db067621242f3f0b8a"], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests["2.2.3"] = (["b31807cb0f88e97f3096e2b378c9815a6acfdc20b0b14f97936d905b536965c4"], CraftHash.HashAlgorithm.SHA256)
        self.patchToApply["2.1.6"] = [("fluidsynth-2.1.6-20210129.diff", 1)]

        self.description = "FluidSynth is a real-time software synthesizer based on the SoundFont 2 specifications and has reached widespread distribution."
        self.webpage = "http://www.fluidsynth.org/"
        self.defaultTarget = "2.2.3"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.buildDependencies["dev-utils/pkg-config"] = None
        self.runtimeDependencies["libs/glib"] = None
        self.runtimeDependencies["libs/libsndfile"] = None


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self, **args):
        super().__init__()
        # dbus support needs a small patch on windows but I have no idea why you would want dbus here
        self.subinfo.options.configure.args = "-DLIB_SUFFIX='' -Denable-dbus=OFF"
