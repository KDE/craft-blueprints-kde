import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets["master"] = "https://github.com/protocolbuffers/protobuf.git"
        self.targetConfigurePath["master"] = "cmake"
        for ver in ["26.1"]:
            self.targets[ver] = f"https://github.com/protocolbuffers/protobuf/archive/v{ver}.tar.gz"
            self.archiveNames[ver] = f"protobuf-{ver}.tar.gz"
            self.targetInstSrc[ver] = f"protobuf-{ver}"
        self.targetDigests["26.1"] = (["4fc5ff1b2c339fb86cd3a25f0b5311478ab081e65ad258c6789359cd84d421f8"], CraftHash.HashAlgorithm.SHA256)
        self.defaultTarget = "26.1"

    def setDependencies(self):
        self.buildDependencies["virtual/base"] = None
        self.buildDependencies["libs/zlib"] = None
        self.buildDependencies["libs/abseil-cpp"] = None


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subinfo.options.dynamic.buildStatic = False
        self.subinfo.options.configure.args += ["-Dprotobuf_BUILD_TESTS=OFF", "-Dprotobuf_MSVC_STATIC_RUNTIME=OFF", "-Dprotobuf_ABSL_PROVIDER=package"]
