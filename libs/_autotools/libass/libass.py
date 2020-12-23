import info

class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["0.15.0"]:
            self.targets[ver] = f"https://github.com/libass/libass/archive/{ver}.tar.gz"
            self.targetInstSrc[ ver ] = "libass-" + ver
        self.targetDigests['0.15.0'] = (['232b1339c633e6a93c153cac7a483e536944921605f35fcbaedc661c62fb49ec'], CraftHash.HashAlgorithm.SHA256)
        self.description = "Portable subtitle renderer"
        self.defaultTarget = '0.15.0'

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

