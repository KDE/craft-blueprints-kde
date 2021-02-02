# -*- coding: utf-8 -*-
import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets['master'] = "https://github.com/ccache/ccache.git"
        self.targetInstallPath["master"] = "dev-utils"

        for ver in ["4.0", "4.1", "4.2"]:
            self.targets[ver] = f"https://github.com/ccache/ccache/releases/download/v{ver}/ccache-{ver}.tar.gz"
            self.targetInstSrc[ver] = f"ccache-{ver}"
            self.targetInstallPath[ver] = "dev-utils"
        self.targetDigests["4.0"] = (['ac97af86679028ebc8555c99318352588ff50f515fc3a7f8ed21a8ad367e3d45'], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests["4.1"] = (['cdeefb827b3eef3b42b5454858123881a4a90abbd46cc72cf8c20b3bd039deb7'], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests["4.2"] = (['dbf139ff32031b54cb47f2d7983269f328df14b5a427882f89f7721e5c411b7e'], CraftHash.HashAlgorithm.SHA256)
        self.patchLevel["4.1"] = 1

        self.webpage = "https://ccache.dev/"
        self.defaultTarget = "4.2"

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
        for t in [Path(os.environ["CXX"]), Path(os.environ["CC"])]:
            if not utils.createShim(self.installDir() / "ccache/bin" / t.name, self.installDir() / f"bin/ccache{CraftCore.compiler.executableSuffix}", args=[t]):
                return False
        return True