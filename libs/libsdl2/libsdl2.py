import info
from CraftCore import CraftCore
from Package.CMakePackageBase import CMakePackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def setTargets(self):
        self.description = "Simple DirectMedia Layer"
        self.webpage = "https://www.libsdl.org"
        for ver in ["2.28.5", "2.30.10"]:
            self.targets[ver] = f"https://www.libsdl.org/release/SDL2-{ver}.tar.gz"
            self.targetInstSrc[ver] = f"SDL2-{ver}"
        self.targetDigests["2.28.5"] = (["332cb37d0be20cb9541739c61f79bae5a477427d79ae85e352089afdaf6666e4"], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests["2.30.10"] = (["f59adf36a0fcf4c94198e7d3d776c1b3824211ab7aeebeb31fe19836661196aa"], CraftHash.HashAlgorithm.SHA256)
        self.defaultTarget = "2.30.10"

    def setDependencies(self):
        self.runtimeDependencies["libs/libsamplerate"] = None
        self.runtimeDependencies["libs/iconv"] = None
        if CraftCore.compiler.platform.isLinux:
            self.runtimeDependencies["libs/pulseaudio"] = None


class Package(CMakePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subinfo.options.configure.args += [
            f"-DSDL_STATIC={self.subinfo.options.buildStatic.asOnOff}",
            "-DSDL_THREADS=ON",
            "-DSDL_DIRECTX=ON",
            "-DSDL_LIBSAMPLERATE=ON",
        ]
        if CraftCore.compiler.platform.isLinux:
            self.subinfo.options.configure.args += ["-DSDL_PULSEAUDIO=ON"]
