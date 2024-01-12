import info
from CraftCore import CraftCore
from Package.CMakePackageBase import CMakePackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def registerOptions(self):
        self.parent.package.categoryInfo.platforms = CraftCore.compiler.Compiler.NoCompiler if CraftCore.compiler.isMSVC() else CraftCore.compiler.Platforms.All

    def setTargets(self):
        self.description = "The Linux Audio Developers Plugin API"
        self.webpage = "http://plugin.org.uk/"

        # Remember to update the CMake patch (at least the project version), when updating to a new version
        for ver in ["1.17"]:
            self.targets[ver] = f"https://www.ladspa.org/download/ladspa_sdk_{ver}.tgz"
            self.targetInstSrc[ver] = f"ladspa_sdk_{ver}/src"
            self.patchToApply[ver] = ("ladspa-sdk-cmake.patch", 0)
        self.targetDigests["1.17"] = (["27d24f279e4b81bd17ecbdcc38e4c42991bb388826c0b200067ce0eb59d3da5b"], CraftHash.HashAlgorithm.SHA256)
        self.patchLevel["1.17"] = 2
        self.defaultTarget = "1.17"

    def setDependencies(self):
        self.buildDependencies["dev-utils/msys"] = None
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/libsndfile"] = None
        if CraftCore.compiler.isWindows:
            self.runtimeDependencies["libs/dlfcn-win32"] = None


class Package(CMakePackageBase):
    def __init__(self, **args):
        super().__init__()
