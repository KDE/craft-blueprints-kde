import info
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["3.11.2"]:
            self.targets[ver] = f"https://github.com/nlohmann/json/releases/download/v{ver}/json.tar.xz"
            self.targetInstSrc[ver] = "json"

        self.targetDigests["3.11.2"] = (["8c4b26bf4b422252e13f332bc5e388ec0ab5c3443d24399acb675e68278d341f"], CraftHash.HashAlgorithm.SHA256)

        self.description = "A library to display png images"
        self.defaultTarget = "3.11.2"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None


class Package(CMakePackageBase):
    def __init__(self, **args):
        super().__init__()
        self.subinfo.options.configure.args += ["-DJSON_BuildTests=OFF"]
