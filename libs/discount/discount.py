import info
from CraftCore import CraftCore
from Package.CMakePackageBase import CMakePackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def registerOptions(self):
        self.options.dynamic.setDefault("buildStatic", CraftCore.compiler.isWindows)

    def setTargets(self):
        self.svnTargets["master"] = "https://github.com/Orc/discount.git"

        for ver in ["2.2.7", "3.0.1.2"]:
            self.targets[ver] = f"https://github.com/Orc/discount/archive/refs/tags/v{ver}.tar.gz"
            self.archiveNames[ver] = f"discount-{ver}.tar.gz"
            self.targetInstSrc[ver] = f"discount-{ver}"
            self.targetConfigurePath[ver] = "cmake"
        self.patchToApply["2.2.7"] = [("create_pc_file_cmake.diff", 1), ("only_lib_fix.diff", 1), ("build-cmake-2.2.7.diff", 1)]

        self.targetDigests["2.2.7"] = (["72c1325ddfc40871d6810f1e272cf2d45b361f26357eb38f170fd04d737bb9f2"], CraftHash.HashAlgorithm.SHA256)
        self.targetDigests["3.0.1.2"] = (["4ea6cc8782c6508b3051c469ed7a1b6ca20b023c2a0c26ccd9c83bc7e61dfc16"], CraftHash.HashAlgorithm.SHA256)
        self.defaultTarget = "3.0.1.2"

        self.releaseManagerId = 12139
        self.webpage = "https://www.pell.portland.or.us/~orc/Code/discount/"
        self.description = "markdown library"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None


class Package(CMakePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subinfo.options.configure.args += ["-DCMAKE_POLICY_VERSION_MINIMUM=3.5", "-DDISCOUNT_ONLY_LIBRARY=ON"]
