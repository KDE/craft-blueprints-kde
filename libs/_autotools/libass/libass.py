import info
from CraftCore import CraftCore
from Package.AutoToolsPackageBase import AutoToolsPackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["0.17.1", "0.17.3"]:
            self.targets[ver] = f"https://github.com/libass/libass/archive/{ver}.tar.gz"
            self.targetInstSrc[ver] = "libass-" + ver
        self.targetDigests["0.17.1"] = (["5ba42655d7e8c5e87bba3ffc8a2b1bc19c29904240126bb0d4b924f39429219f"], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests["0.17.3"] = (["26fbfb7a7bd3e6d5c713f8a65a12b36084d1dde6efaed8a9996489054c4aeca0"], CraftHash.HashAlgorithm.SHA256)
        self.description = "Portable subtitle renderer"
        self.defaultTarget = "0.17.3"

    def setDependencies(self):
        self.buildDependencies["dev-utils/nasm"] = None
        self.runtimeDependencies["libs/fontconfig"] = None
        self.runtimeDependencies["libs/freetype"] = None
        self.runtimeDependencies["libs/fribidi"] = None
        self.runtimeDependencies["libs/harfbuzz"] = None


class Package(AutoToolsPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        if CraftCore.compiler.platform.isAndroid:
            self.subinfo.options.configure.args += ["--disable-require-system-font-provider"]
