import info


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["0.17.1"]:
            self.targets[ver] = f"https://github.com/libass/libass/archive/{ver}.tar.gz"
            self.targetInstSrc[ver] = "libass-" + ver
        self.targetDigests["0.17.1"] = (["5ba42655d7e8c5e87bba3ffc8a2b1bc19c29904240126bb0d4b924f39429219f"], CraftHash.HashAlgorithm.SHA256)
        self.description = "Portable subtitle renderer"
        self.defaultTarget = "0.17.1"

    def setDependencies(self):
        self.buildDependencies["dev-utils/nasm"] = None
        self.runtimeDependencies["libs/fontconfig"] = None
        self.runtimeDependencies["libs/freetype"] = None
        self.runtimeDependencies["libs/fribidi"] = None
        self.runtimeDependencies["libs/harfbuzz"] = None


from Package.AutoToolsPackageBase import *


class Package(AutoToolsPackageBase):
    def __init__(self, **args):
        AutoToolsPackageBase.__init__(self)
        self.subinfo.options.configure.args += " --disable-static --enable-shared "

        if CraftCore.compiler.isAndroid:
            self.subinfo.options.configure.args += " --disable-require-system-font-provider "
