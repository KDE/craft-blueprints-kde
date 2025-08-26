import info
from CraftCore import CraftCore
from Package.CMakePackageBase import CMakePackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def registerOptions(self):
        self.options.dynamic.setDefault("buildTools", False)

    def setTargets(self):
        self.description = "An open, royalty-free video coding format designed for video transmissions over the Internet"
        for ver in ["3.12.1"]:
            self.targets[ver] = f"https://storage.googleapis.com/aom-releases/libaom-{ver}.tar.gz"
            self.targetInstSrc[ver] = f"libaom-{ver}"
        self.targetDigests["3.12.1"] = (["9e9775180dec7dfd61a79e00bda3809d43891aee6b2e331ff7f26986207ea22e"], CraftHash.HashAlgorithm.SHA256)
        self.defaultTarget = "3.12.1"

    def setDependencies(self):
        self.buildDependencies["dev-utils/cmake"] = None
        self.buildDependencies["dev-utils/perl"] = None
        self.buildDependencies["dev-utils/nasm"] = None
        self.runtimeDependencies["virtual/base"] = None


class Package(CMakePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subinfo.options.configure.args += [
            "-DENABLE_DOCS=OFF",
            "-DENABLE_NASM=ON",
            "-DCONFIG_PIC=1",
            "-DENABLE_EXAMPLES=OFF",
            f"-DENABLE_TESTS={self.subinfo.options.dynamic.buildTests.asOnOff}",
            f"-DENABLE_TOOLS={self.subinfo.options.dynamic.buildTools.asOnOff}",
            f"-DAOM_TARGET_CPU={CraftCore.compiler.architecture.name.lower()}",
        ]
        if CraftCore.compiler.androidAbi == "armeabi-v7a":
            # building libwebm fails on Android ARM32; disable it
            self.subinfo.options.configure.args += [
                "-DCONFIG_WEBM_IO=0",
                "-DAOM_TARGET_CPU=armv7a",
            ]
