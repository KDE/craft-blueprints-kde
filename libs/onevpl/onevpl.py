import info


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["2023.2.1"]:
            self.targets[ver] = f"https://github.com/oneapi-src/oneVPL/archive/refs/tags/v{ver}.tar.gz"
            self.targetInstSrc[ver] = "oneVPL-" + ver
        self.targetDigests["2023.2.1"] = (["28dcffb6752a715bf063cea5f368f9633d3b92807ae83a5bb47305d4c7c4c899"], CraftHash.HashAlgorithm.SHA256)
        self.description = "oneVPL Video Processing Library"
        self.defaultTarget = "2023.2.1"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.buildDependencies["dev-utils/nasm"] = None


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self, **args):
        CMakePackageBase.__init__(self)
        self.subinfo.options.configure.args = "-DINSTALL_EXAMPLE_CODE=OFF -DBUILD_TOOLS=OFF -DENABLE_WAYLAND=OFF"
