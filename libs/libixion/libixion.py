import info
from Package.AutoToolsPackageBase import AutoToolsPackageBase
from Utils import CraftHash

class subinfo(info.infoclass):
    def setTargets(self):
        self.description = "a general purpose formula parser, interpreter, formula cell dependency tracker and spreadsheet document model backend all in one package"

        for ver in ["0.19.0"]:
            self.targets[ver] = f"https://gitlab.com/api/v4/projects/ixion%2Fixion/packages/generic/source/{ver}/libixion-{ver}.tar.xz"
            self.targetInstSrc[ver] = f"libixion-{ver}"
        self.targetDigests["0.19.0"] = (["b4864d7a55351a09adbe9be44e5c65b1d417e80e946c947951d0e8428b9dcd15"], CraftHash.HashAlgorithm.SHA256)

        self.defaultTarget = "0.19.0"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.buildDependencies["libs/boost/boost-system"] = None
        self.buildDependencies["libs/boost/boost-filesystem"] = None
        self.buildDependencies["libs/mdds"] = None


class Package(AutoToolsPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        #self.subinfo.options.configure.args += ["--disable-static", "--enable-shared"]
