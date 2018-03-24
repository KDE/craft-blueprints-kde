# -*- coding: utf-8 -*-

import info


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["5.0.5"]:
            self.targets[ver] = f"http://tukaani.org/xz/xz-" + ver + ".tar.xz"
            self.targetInstSrc[ver] = "xz-" + ver
            self.patchToApply[ver] = [("xz-5.0.5.diff", 1), ("xz-cmake-5.0.5.diff", 1)]
            self.targetDigests["5.0.5"] = "56f1d78117f0c32bbb1cfd40117aa7f55bee8765"

        self.description = "free general-purpose data compression software with high compression ratio"
        self.defaultTarget = ver

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = "default"


from Package.CMakePackageBase import *


class PackageCMake(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)


from Package.AutoToolsPackageBase import *

class PackageAutotools(AutoToolsPackageBase):
    def __init__( self, **args ):
        AutoToolsPackageBase.__init__( self )
        self.subinfo.options.configure.args += " --disable-static --enable-shared "




if CraftCore.compiler.isWindows:
    class Package(PackageCMake):
        pass
else:
    class Package(PackageAutotools):
        pass
