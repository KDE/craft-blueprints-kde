import info
import utils
from CraftCore import CraftCore
from Package.CMakePackageBase import CMakePackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def registerOptions(self):
        # MSVC is not well supported by frei0r-plugins, and it currently does not compile there so skip building it
        # This is not a major deal as the main user is Kdenlive and it has other dependencies that are MingW only
        if CraftCore.compiler.isMSVC():
            self.parent.package.categoryInfo.platforms = CraftCore.compiler.Compiler.NoCompiler

    def setTargets(self):
        self.description = "Minimalistic plugin API for video effects, plugins collection"
        self.webpage = "http://frei0r.dyne.org/"
        for ver in ["2.5.0"]:
            self.targets[ver] = f"https://github.com/dyne/frei0r/archive/v{ver}.tar.gz"
            self.targetInstSrc[ver] = f"frei0r-{ver}"
        self.targetDigests["2.5.0"] = (["6ce8e9c1fd721c183c9524bd12f397f04121dd5bb655ee7c7d38d0dfa50faa23"], CraftHash.HashAlgorithm.SHA256)

        self.svnTargets["master"] = "https://github.com/dyne/frei0r.git"
        self.defaultTarget = "2.5.0"

    def setDependencies(self):
        # TODO MSVC: it looks as if cairo and gavl are not detected

        self.runtimeDependencies["virtual/base"] = None
        if not CraftCore.compiler.isMSVC():
            # TODO check why build fails with OpenCV, shouldn't be too hard to fix
            self.runtimeDependencies["libs/opencv/opencv"] = None
        self.runtimeDependencies["libs/cairo"] = None
        # if not CraftCore.compiler.isMacOS:
        self.runtimeDependencies["libs/gavl"] = None


class Package(CMakePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # if CraftCore.compiler.isMacOS:
        #    self.subinfo.options.configure.args += ["-DWITHOUT_GAVL=1"]

        # TODO check why build fails with OpenCV, shouldn't be too hard to fix
        if CraftCore.compiler.isMSVC():
            self.subinfo.options.configure.args += ["-DWITHOUT_OPENCV=1"]

    def install(self):
        if not super().install():
            return False
        if CraftCore.compiler.isMacOS:
            return utils.mergeTree(self.installDir() / "lib/frei0r-1", self.installDir() / "plugins/frei0r-1")
        return True
