import info
from Package.CMakePackageBase import *
from CraftCore import CraftCore


class subinfo(info.infoclass):
    def setTargets(self):
        self.description = "An open, royalty-free video coding format designed for video transmissions over the Internet"
        for ver in ["3.1.3", "3.6.1", "3.8.2"]:
            self.targets[ver] = f"https://storage.googleapis.com/aom-releases/libaom-{ver}.tar.gz"
            self.targetInstSrc[ver] = f"libaom-{ver}"
        self.targetDigests["3.8.2"] = (["98f7d6d7ddbf06d088735f5e51782df053fd1b08c553882c2924bd0b2021a202"], CraftHash.HashAlgorithm.SHA256)
        self.defaultTarget = "3.8.2"

    def setDependencies(self):
        self.buildDependencies["dev-utils/cmake"] = None
        self.buildDependencies["dev-utils/perl"] = None
        self.buildDependencies["dev-utils/nasm"] = None
        self.runtimeDependencies["virtual/base"] = None


class Package(CMakePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subinfo.options.dynamic.buildStatic = False
        self.subinfo.options.configure.args += [
            "-DENABLE_DOCS=OFF",
            "-DENABLE_NASM=ON",
            "-DCONFIG_PIC=1",
            "-DENABLE_EXAMPLES=OFF",
            "-DENABLE_TESTS=OFF",
            f"-DAOM_TARGET_CPU={CraftCore.compiler.architecture.name.lower()}",
        ]
        if CraftCore.compiler.androidAbi == "armeabi-v7a":
            # building libwebm fails on Android ARM32; disable it
            self.subinfo.options.configure.args += ["-DCONFIG_WEBM_IO=0", "-DAOM_TARGET_CPU=armv7a",]
