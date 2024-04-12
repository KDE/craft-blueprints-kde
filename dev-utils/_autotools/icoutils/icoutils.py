import info


class subinfo(info.infoclass):
    def registerOptions(self):
        self.parent.package.categoryInfo.platforms = CraftCore.compiler.Platforms.NotMacOS

    def setTargets(self):
        for ver in ["0.32.3"]:
            self.targets[ver] = f"https://savannah.nongnu.org/download/icoutils/icoutils-{ver}.tar.bz2"
            self.targetInstSrc[ver] = f"icoutils-{ver}"

        self.targetDigests["0.32.3"] = (["17abe02d043a253b68b47e3af69c9fc755b895db68fdc8811786125df564c6e0"], CraftHash.HashAlgorithm.SHA256)
        self.description = "The icoutils are a set of command-line programs for extracting and converting images in Microsoft Windows(R) icon and cursor files."
        self.webpage = "https://www.nongnu.org/icoutils/"
        self.defaultTarget = "0.32.3"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.buildDependencies["dev-utils/msys"] = None
        self.runtimeDependencies["libs/libpng"] = None
        self.runtimeDependencies["libs/gettext"] = None


from Package.AutoToolsPackageBase import *


class Package(AutoToolsPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subinfo.options.configure.autoreconf = False
