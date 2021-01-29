import info


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["2.1.6"]:
            self.targets[ver] = f"https://github.com/FluidSynth/fluidsynth/archive/v{ver}.tar.gz"
            self.targetInstSrc[ver] = f"fluidsynth-{ver}"
        self.targetDigests['2.1.6'] = (['328fc290b5358544d8dea573f81cb1e97806bdf49e8507db067621242f3f0b8a'], CraftHash.HashAlgorithm.SHA256)
        self.patchToApply["2.1.6"] = [("fluidsynth-2.1.6-20210129.diff", 1)]

        self.description = "FluidSynth is a real-time software synthesizer based on the SoundFont 2 specifications and has reached widespread distribution."
        self.webpage = "http://www.fluidsynth.org/"
        self.defaultTarget = '2.1.6'

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.buildDependencies["dev-utils/pkg-config"] = None
        self.runtimeDependencies["libs/glib"] = None
        self.runtimeDependencies["libs/libsndfile"] = None


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self, **args):
        CMakePackageBase.__init__(self)
        # dbus support needs a small patch on windows but I have no idea why you would want dbus here
        self.subinfo.options.configure.args = "-DLIB_SUFFIX='' -Denable-dbus=OFF"
