import info


class subinfo(info.infoclass):
    def registerOptions(self):
        self.parent.package.categoryInfo.platforms = CraftCore.compiler.Compiler.NoCompiler if CraftCore.compiler.isMSVC() else CraftCore.compiler.Platforms.All

    def setTargets(self):
        self.description = "The Linux Audio Developers Plugin API"
        self.webpage = "http://plugin.org.uk/"
        for ver in ["1.17"]:
            self.targets[ver] = "http://www.ladspa.org/download/ladspa_sdk_" + ver + ".tgz"
            self.targetInstSrc[ver] = "ladspa_sdk_" + ver + "/src"
            self.patchToApply[ver] = ("ladspa-sdk-cmake.patch", 0)
        self.targetDigests["1.17"] = (["27d24f279e4b81bd17ecbdcc38e4c42991bb388826c0b200067ce0eb59d3da5b"], CraftHash.HashAlgorithm.SHA256)
        self.defaultTarget = "1.17"

    def setDependencies(self):
        self.buildDependencies["dev-utils/msys"] = None
        self.runtimeDependencies["virtual/base"] = None
        if OsUtils.isWin():
            self.runtimeDependencies["libs/dlfcn-win32"] = None


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self, **args):
        CMakePackageBase.__init__(self)
