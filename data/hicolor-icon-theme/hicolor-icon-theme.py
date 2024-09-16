import info
import utils
from Package.CMakePackageBase import CMakePackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def setTargets(self):
        for v in ["0.15"]:
            self.targets[v] = f"https://icon-theme.freedesktop.org/releases/hicolor-icon-theme-{v}.tar.xz"
        self.targetDigests["0.15"] = (["9cc45ac3318c31212ea2d8cb99e64020732393ee7630fa6c1810af5f987033cc"], CraftHash.HashAlgorithm.SHA256)
        self.description = "High-color icon theme shell from the FreeDesktop project"
        self.defaultTarget = "0.15"

    def setDependencies(self):
        self.buildDependencies["virtual/base"] = None


class Package(CMakePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def configure(self):
        return True

    def make(self):
        return True

    def install(self):
        hicolorDir = self.imageDir() / "share/icons/hicolor"
        utils.createDir(hicolorDir)
        utils.copyFile(self.sourceDir() / f"hicolor-icon-theme-{self.version}/index.theme", hicolorDir / "index.theme")
        return True
