import info
from Package.CMakePackageBase import CMakePackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["3.11.2", "3.12.0"]:
            self.targets[ver] = f"https://github.com/nlohmann/json/releases/download/v{ver}/json.tar.xz"
            self.archiveNames[ver] = f"json-{ver}.tar.xz"
            self.targetInstSrc[ver] = "json"

        self.targetDigests["3.11.2"] = (["8c4b26bf4b422252e13f332bc5e388ec0ab5c3443d24399acb675e68278d341f"], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests["3.12.0"] = (["42f6e95cad6ec532fd372391373363b62a14af6d771056dbfc86160e6dfff7aa"], CraftHash.HashAlgorithm.SHA256)

        self.description = "A library to display png images"
        self.defaultTarget = "3.12.0"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None


class Package(CMakePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subinfo.options.configure.args += ["-DJSON_BuildTests=OFF"]
