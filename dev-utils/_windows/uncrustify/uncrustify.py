import info
import utils
from Package.CMakePackageBase import CMakePackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets["master"] = "https://github.com/uncrustify/uncrustify.git"
        self.targetInstallPath["master"] = "dev-utils/uncrustify"
        for ver in ["0.64"]:
            self.targets[ver] = f"https://github.com/uncrustify/uncrustify/archive/uncrustify-{ver}.tar.gz"
            self.targetInstSrc[ver] = f"uncrustify-uncrustify-{ver}"
            self.targetInstallPath[ver] = "dev-utils/uncrustify"
        self.targetDigests["0.64"] = (["2a8cb3ab82ca53202d50fc2c2cec0edd11caa584def58d356c1c759b57db0b32"], CraftHash.HashAlgorithm.SHA256)

        self.description = "Source Code Beautifier for C, C++, C#, ObjectiveC, D, Java, Pawn and VALA"
        self.webpage = "https://uncrustify.sourceforge.net/"
        self.defaultTarget = "0.64"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None


class Package(CMakePackageBase):
    def __init__(self, **args):
        super().__init__()

    def install(self):
        if not super().install():
            return False
        return utils.createShim(self.imageDir() / "dev-utils/bin/uncrustify.exe", self.imageDir() / "dev-utils/uncrustify/uncrustify.exe")
