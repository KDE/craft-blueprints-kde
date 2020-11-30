# -*- coding: utf-8 -*-
import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets['master'] = "https://github.com/jrosdahl/ccache.git"
        self.targetInstallPath["master"] = "dev-utils"

        for ver in ["4.0", "4.1"]:
            self.targets[ver] = f"https://github.com/ccache/ccache/releases/download/v{ver}/ccache-{ver}.tar.gz"
            self.targetInstSrc[ver] = f"ccache-{ver}"
            self.targetInstallPath[ver] = "dev-utils"
        self.targetDigests["4.0"] = (['ac97af86679028ebc8555c99318352588ff50f515fc3a7f8ed21a8ad367e3d45'], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests["4.1"] = (['cdeefb827b3eef3b42b5454858123881a4a90abbd46cc72cf8c20b3bd039deb7'], CraftHash.HashAlgorithm.SHA256)

        self.webpage = "https://ccache.dev/"
        self.defaultTarget = "4.1"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/libzstd"] = None
        if CraftCore.compiler.isMinGW():
            self.buildDependencies["dev-utils/msys"] = None


from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__(self, **args):
        CMakePackageBase.__init__(self)
        self.supportsCCACHE = False
        if CraftCore.compiler.isMinGW:
            self.subinfo.options.configure.args += ["-DCMAKE_C_FLAGS=-fno-asynchronous-unwind-tables"]

    def install(self):
        if not super().install():
            return False
        if CraftCore.compiler.isGCC:
            targets = ["gcc", "g++", "cpp", "c++"]
        elif CraftCore.compiler.isClang:
            targets = ["clang", "clang++"]
        for t in targets:
            arg = CraftCore.cache.findApplication(t)
            if not utils.createShim(self.installDir() / "ccache/bin" / t, self.installDir() / f"bin/ccache{CraftCore.compiler.executableSuffix}", args=[arg]):
                return False
        return True