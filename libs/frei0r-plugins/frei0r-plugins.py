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

        self.svnTargets["f7b0adb"] = "https://github.com/dyne/frei0r.git||f7b0adb31765a8b7f900db1f690cecf91921c2f5"
        # https://github.com/dyne/frei0r/pull/280, https://github.com/dyne/frei0r/pull/281
        self.patchToApply["f7b0adb"] = [("280.patch", 1), ("280.patch", 1)]
        self.patchLevel["f7b0adb"] = 1

        self.defaultTarget = "f7b0adb"

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
