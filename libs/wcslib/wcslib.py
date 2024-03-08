import info
from CraftCore import CraftCore
from Package.CMakePackageBase import CMakePackageBase


class subinfo(info.infoclass):
    def setTargets(self):
        self.description = "World Coordinate System Library"

        for ver in ["7.7"]:
            self.targets[ver] = f"https://indilib.org/jdownloads/wcslib/wcslib-{ver}.tar.gz"
            self.targetInstSrc[ver] = f"wcslib-{ver}"

        if not CraftCore.compiler.isWindows:
            self.patchToApply["7.7"] = [("int64.diff", 1)]

        self.patchLevel["7.7"] = 2

        self.defaultTarget = "7.7"

    def setDependencies(self):
        self.runtimeDependencies["libs/cfitsio"] = None


class Package(CMakePackageBase):
    def __init__(self):
        super().__init__()
        self.subinfo.options.configure.args += ["-DCMAKE_POSITION_INDEPENDENT_CODE=ON"]
