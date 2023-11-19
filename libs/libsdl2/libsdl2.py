import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.description = "Simple DirectMedia Layer"
        self.webpage = "https://www.libsdl.org"
        for ver in ["2.26.4", "2.28.4"]:
            self.targets[ver] = f"https://www.libsdl.org/release/SDL2-{ver}.tar.gz"
            self.targetInstSrc[ver] = f"SDL2-{ver}"
        self.targetDigests["2.26.4"] = (["1a0f686498fb768ad9f3f80b39037a7d006eac093aad39cb4ebcc832a8887231"], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests["2.28.4"] = (["888b8c39f36ae2035d023d1b14ab0191eb1d26403c3cf4d4d5ede30e66a4942c"], CraftHash.HashAlgorithm.SHA256)
        self.defaultTarget = "2.28.4"

    def setDependencies(self):
        self.runtimeDependencies["libs/libsamplerate"] = None
        self.runtimeDependencies["libs/iconv"] = None
        if CraftCore.compiler.isLinux:
            self.runtimeDependencies["libs/_linux/pulseaudio"] = None


from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__(self, **args):
        CMakePackageBase.__init__(self)
        self.subinfo.options.configure.args += ["-DSDL_STATIC=OFF", "-DSDL_THREADS=ON", "-DSDL_DIRECTX=ON", "-DSDL_LIBSAMPLERATE=ON"]
        if CraftCore.compiler.isLinux:
            self.subinfo.options.configure.args += ["-DSDL_PULSEAUDIO=ON"]
