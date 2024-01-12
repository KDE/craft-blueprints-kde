import info
from CraftCore import CraftCore
from Package.CMakePackageBase import CMakePackageBase


class subinfo(info.infoclass):
    def registerOptions(self):
        self.parent.package.categoryInfo.compiler = CraftCore.compiler.Compiler.CL

    def setTargets(self):
        for ver in ["2.8.0", "2.9.1"]:
            ver2 = ver.replace(".", "-")
            self.targets[ver] = f"ftp://sourceware.org/pub/pthreads-win32/pthreads-w32-{ver2}-release.tar.gz"
            self.targetInstSrc[ver] = f"pthreads-w32-{ver2}-release"

        self.patchToApply["2.8.0"] = [("pthreads-w32-2-8-0-release-20110729.diff", 1)]
        self.patchToApply["2.9.1"] = [("pthreads-w32-2-9-1-release-20130901.diff", 1)]
        self.targetDigests["2.8.0"] = "da8371cb20e8e238f96a1d0651212f154d84a9ac"
        self.targetDigests["2.9.1"] = "24d40e89c2e66a765733e8c98d6f94500343da86"

        self.description = "a POSIX thread implementation for windows"
        self.defaultTarget = "2.9.1"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None


class Package(CMakePackageBase):
    def __init__(self, **args):
        super().__init__()
        self.subinfo.options.configure.args += ["-DBUILD_TESTS=OFF"]
