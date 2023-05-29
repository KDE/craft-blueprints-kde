import info
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets["master"] = "https://github.com/Orc/discount.git"

        for ver in ["2.2.7"]:
            self.targets[ver] = "https://github.com/Orc/discount/archive/refs/tags/v%s.tar.gz" % ver
            self.archiveNames[ver] = "discount-%s.tar.gz" % ver
            self.targetInstSrc[ver] = "discount-%s" % ver
            self.targetConfigurePath[ver] = "cmake"
            self.patchToApply[ver] = [("create_pc_file_cmake.diff", 1), ("only_lib_fix.diff", 1), ("build-cmake-2.2.7.diff", 1)]

        self.targetDigests["2.2.7"] = (["72c1325ddfc40871d6810f1e272cf2d45b361f26357eb38f170fd04d737bb9f2"], CraftHash.HashAlgorithm.SHA256)

        self.defaultTarget = "2.2.7"
        self.description = "markdown library"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None


class Package(CMakePackageBase):
    def __init__(self, **args):
        CMakePackageBase.__init__(self)
        self.subinfo.options.configure.args += "-DDISCOUNT_ONLY_LIBRARY=ON"
        if CraftCore.compiler.isWindows:
            self.subinfo.options.configure.args += "-DBUILD_SHARED_LIBS=OFF"
