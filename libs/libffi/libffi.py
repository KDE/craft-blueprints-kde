import info

from Package.CMakePackageBase import CMakePackageBase


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["3.3"]:
            self.targets[ver] = f"https://github.com/libffi/libffi/releases/download/v{ver}/libffi-{ver}.tar.gz"
            self.targetInstSrc[ver] = f"libffi-{ver}"
        if not CraftCore.compiler.isGCCLike():
            self.patchToApply["3.3"] = [("535.patch", 1), # https://github.com/libffi/libffi/pull/535
                                        ("libffi-3.3-20201216.diff",1)
            ]
        self.patchLevel["3.3"] = 1
        self.defaultTarget = "3.3"

    def setDependencies(self):
        self.buildDependencies["virtual/base"] = None
        self.buildDependencies["dev-utils/msys"] = None


class PackageCMake(CMakePackageBase):
    def __init__(self, **args):
        CMakePackageBase.__init__(self)

from Package.AutoToolsPackageBase import *


class PackageAutoTools(AutoToolsPackageBase):
    def __init__(self):
        AutoToolsPackageBase.__init__(self)
        self.subinfo.options.configure.args += ["--enable-shared", "--disable-static"]


if CraftCore.compiler.isGCCLike():
    class Package(PackageAutoTools):
        pass
else:
    class Package(PackageCMake):
        pass
