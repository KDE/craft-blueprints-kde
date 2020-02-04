import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets['master'] = 'https://github.com/protocolbuffers/protobuf.git'
        self.targetConfigurePath["master"] = "cmake"
        for ver in ["3.11.2"]:
            self.targets[ver] = f"https://github.com/protocolbuffers/protobuf/archive/v{ver}.tar.gz"
            self.archiveNames[ver] = f"protobuf-{ver}.tar.gz"
            self.targetInstSrc[ver] = f"protobuf-{ver}"
            self.targetConfigurePath[ver] = "cmake"
        self.targetDigests["3.11.2"] = (['e8c7601439dbd4489fe5069c33d374804990a56c2f710e00227ee5d8fd650e67'], CraftHash.HashAlgorithm.SHA256)
        self.defaultTarget = "3.11.2"

    def setDependencies(self):
        self.buildDependencies["virtual/base"] = None
        self.buildDependencies["libs/zlib"] = None

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
        self.subinfo.options.configure.args += " -Dprotobuf_BUILD_TESTS=OFF -Dprotobuf_MSVC_STATIC_RUNTIME=OFF"
        if not CraftCore.compiler.isWindows:
            self.subinfo.options.configure.args += " -DBUILD_SHARED_LIBS=ON"