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

        self.svnTargets["cfce4bc"] = "https://github.com/dyne/frei0r.git||cfce4bcc2ed0a38b7f01483008700aeb94558428"
        self.patchToApply["cfce4bc"] = [
            # https://github.com/dyne/frei0r/pull/285
            ("285.patch", 1),
            ("scale0tilt-without-gavl.patch", 1),
        ]

        if CraftCore.compiler.compiler.isMSVC:
            self.patchToApply["cfce4bc"] += [("fix-msvc.diff", 1)]

        self.defaultTarget = "cfce4bc"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/cairo"] = None
        # Disable gavl. See note below on self.subinfo.options.configure.args for details.
        # self.runtimeDependencies["libs/gavl"] = None


class Package(CMakePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.subinfo.options.configure.args += [
            # Disable gavl because it is annoying to deal with and it is only required for
            # scal0tilt, rgbparade and vectorscope. However for scale0tilt we have a patch above.
            # The other two are not that important given Kdenlive as buildin rgbpade and vectorscope.
            # f"-DWITHOUT_GAVL={self.subinfo.options.isActive('libs/gavl').inverted.asOnOff}",
            "-DWITHOUT_GAVL=OFF",
            # Disable OpenCV as it can cause protobuf conflicts and is only
            # used in facebl0r / facedetect which do not work in Kdenlive
            "-DWITHOUT_OPENCV=ON",
            f"-DWITHOUT_CAIRO={self.subinfo.options.isActive('libs/cairo').inverted.asOnOff}",
        ]

    def install(self):
        if not super().install():
            return False
        if CraftCore.compiler.platform.isMacOS:
            return utils.mergeTree(self.installDir() / "lib/frei0r-1", self.installDir() / "plugins/frei0r-1")
        return True
