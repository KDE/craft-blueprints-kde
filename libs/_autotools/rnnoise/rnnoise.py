import info
from CraftCore import CraftCore
from Package.AutoToolsPackageBase import AutoToolsPackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets["0.2"] = "https://github.com/xiph/rnnoise.git||v0.2"
        self.defaultTarget = "0.2"
        self.description = "A noise suppression library based on a recurrent neural network"
        self.webpage = "https://github.com/xiph/rnnoise"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None


class Package(AutoToolsPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subinfo.options.configure.args += ["--enable-shared", "--disable-static"]
