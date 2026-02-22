import info
import utils
from CraftCore import CraftCore
from Package.CMakePackageBase import CMakePackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def setTargets(self):
        self.description = "Minimalistic plugin API for video effects, plugins collection"
        self.webpage = "http://frei0r.dyne.org/"
        for ver in ["2.5.0"]:
            self.targets[ver] = f"https://github.com/dyne/frei0r/archive/v{ver}.tar.gz"
            self.targetInstSrc[ver] = f"frei0r-{ver}"
        self.targetDigests["2.5.0"] = (["c511aeb51faeb0de2afe47327c30026d5b76ccc910a0b93d286029f07d29c656"], CraftHash.HashAlgorithm.SHA256)

        self.svnTargets["master"] = "https://github.com/dyne/frei0r.git"
        self.svnTargets["eb52a11"] = "https://github.com/dyne/frei0r.git||eb52a11df3e8675016dfb15d757f6d805228114a"
        self.defaultTarget = "eb52a11"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/opencv/opencv"] = None
        self.runtimeDependencies["libs/cairo"] = None
        self.runtimeDependencies["libs/gavl"] = None


class Package(CMakePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.subinfo.options.configure.args += [
            f"-DWITHOUT_GAVL={self.subinfo.options.isActive('libs/gavl').inverted.asOnOff}",
            f"-DWITHOUT_OPENCV={self.subinfo.options.isActive('libs/opencv').inverted.asOnOff}",
            f"-DWITHOUT_CAIRO={self.subinfo.options.isActive('libs/cairo').inverted.asOnOff}",
        ]

    def install(self):
        if not super().install():
            return False
        if CraftCore.compiler.isMacOS:
            return utils.mergeTree(self.installDir() / "lib/frei0r-1", self.installDir() / "plugins/frei0r-1")
        return True
