# -*- coding: utf-8 -*-
import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets['master'] = "https://github.com/ccache/ccache.git"
        self.targetInstallPath["master"] = "dev-utils"

        for ver in ["4.4.2"]:
            self.targets[ver] = f"https://github.com/ccache/ccache/releases/download/v{ver}/ccache-{ver}.tar.gz"
            self.targetInstSrc[ver] = f"ccache-{ver}"
            self.targetInstallPath[ver] = "dev-utils"
        self.targetDigests["4.4.2"] = (['357a2ac55497b39ad6885c14b00cda6cf21d1851c6290f4288e62972665de417'], CraftHash.HashAlgorithm.SHA256)

        self.webpage = "https://ccache.dev/"
        self.defaultTarget = "4.4.2"

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
        self.subinfo.options.configure.args += ["-DREDIS_STORAGE_BACKEND=OFF"]

    def install(self):
        if not super().install():
            return False
        for t in [Path(os.environ["CXX"]), Path(os.environ["CC"])]:
            if not utils.createShim(self.installDir() / "ccache/bin" / t.name, self.installDir() / f"bin/ccache{CraftCore.compiler.executableSuffix}", args=[t]):
                return False
        return True