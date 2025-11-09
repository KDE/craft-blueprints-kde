import info
from Package.CMakePackageBase import CMakePackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["1.0.31"]:
            self.targets[ver] = f"https://github.com/libsndfile/libsndfile/releases/download/{ver}/libsndfile-{ver}.tar.bz2"
            self.targetInstSrc[ver] = f"libsndfile-{ver}"
        for ver in ["1.2.2"]:
            self.targets[ver] = f"https://github.com/libsndfile/libsndfile/releases/download/{ver}/libsndfile-{ver}.tar.xz"
            self.targetInstSrc[ver] = f"libsndfile-{ver}"
        self.targetDigests["1.0.31"] = (["a8cfb1c09ea6e90eff4ca87322d4168cdbe5035cb48717b40bf77e751cc02163"], CraftHash.HashAlgorithm.SHA256)
        self.patchLevel["1.0.31"] = 1
        self.targetDigests["1.2.2"] = (["3799ca9924d3125038880367bf1468e53a1b7e3686a934f098b7e1d286cdb80e"], CraftHash.HashAlgorithm.SHA256)

        self.description = "A C library for reading and writing files containing sampled sound"
        self.webpage = "https://github.com/libsndfile/libsndfile/"
        self.releaseManagerId = 13277
        self.defaultTarget = "1.2.2"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/libogg"] = None
        self.runtimeDependencies["libs/libvorbis"] = None
        self.runtimeDependencies["libs/libflac"] = None
        self.runtimeDependencies["libs/libopus"] = None


class Package(CMakePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # self.subinfo.options.configure.args += ["-DENABLE_COMPATIBLE_LIBSNDFILE_NAME=ON"]
        self.subinfo.options.configure.args += ["-DCMAKE_POLICY_VERSION_MINIMUM=3.5"]
