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
        self.svnTargets["32e9140"] = "https://github.com/dyne/frei0r.git||32e91405d2ec5e222f75175b36dc4cc7bc0667ef"
        self.patchLevel["32e9140"] = 1
        self.defaultTarget = "32e9140"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/cairo"] = None
        self.runtimeDependencies["libs/gavl"] = None


class Package(CMakePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Disable OpenCV as it can cause protobuf conflicts and is only
        # used in facebl0r / facedetect which do not work in Kdenlive
        self.subinfo.options.configure.args += [
            f"-DWITHOUT_GAVL={self.subinfo.options.isActive('libs/gavl').inverted.asOnOff}",
            "-DWITHOUT_OPENCV=ON",
            f"-DWITHOUT_CAIRO={self.subinfo.options.isActive('libs/cairo').inverted.asOnOff}",
        ]

    def install(self):
        if not super().install():
            return False
        if CraftCore.compiler.isMacOS:
            return utils.mergeTree(self.installDir() / "lib/frei0r-1", self.installDir() / "plugins/frei0r-1")
        return True
