import info
from Package.CMakePackageBase import CMakePackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def registerOptions(self):
        # something is missing in abseil
        self.options.dynamic.setDefault("buildTests", False)

    def setTargets(self):
        self.svnTargets["master"] = "https://github.com/protocolbuffers/protobuf.git"
        self.targetConfigurePath["master"] = "cmake"
        for ver in ["26.1", "33.0"]:
            self.targets[ver] = f"https://github.com/protocolbuffers/protobuf/archive/v{ver}.tar.gz"
            self.archiveNames[ver] = f"protobuf-{ver}.tar.gz"
            self.targetInstSrc[ver] = f"protobuf-{ver}"
        self.targetDigests["26.1"] = (["4fc5ff1b2c339fb86cd3a25f0b5311478ab081e65ad258c6789359cd84d421f8"], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests["33.0"] = (["b6b03fbaa3a90f3d4f2a3fa4ecc41d7cd0326f92fcc920a7843f12206c8d52cd"], CraftHash.HashAlgorithm.SHA256)
        self.defaultTarget = "33.0"

        self.description = "Protocol Buffers - Google's data interchange format"
        self.webpage = "https://protobuf.dev/"
        self.releaseManagerId = 3715

    def setDependencies(self):
        self.buildDependencies["virtual/base"] = None
        self.buildDependencies["libs/zlib"] = None
        self.runtimeDependencies["libs/abseil-cpp"] = None


class Package(CMakePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subinfo.options.configure.args += [
            f"-Dprotobuf_BUILD_TESTS={self.subinfo.options.dynamic.buildTests.asOnOff}",
            "-Dprotobuf_MSVC_STATIC_RUNTIME=OFF",
            "-Dprotobuf_ABSL_PROVIDER=package",
        ]
