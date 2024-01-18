import info
from Package.CMakePackageBase import CMakePackageBase


class subinfo(info.infoclass):
    def setTargets(self):
        self.description = "a library for dealing with Microsoft ITSS/CHM format files"

        for ver in ["0.40"]:
            # the server does not support https
            self.targets[ver] = f"http://www.jedrea.com/chmlib/chmlib-{ver}.tar.bz2"
            self.targetInstSrc[ver] = f"chmlib-{ver}"
        self.patchToApply["0.40"] = ("chm-cmake.diff", 0)
        self.patchLevel["0.40"] = 1
        self.targetDigests["0.40"] = "5231d7531e8808420d7f89fd1e4fdbac1ed7a167"

        self.defaultTarget = "0.40"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None


class Package(CMakePackageBase):
    def __init__(self, **args):
        super().__init__()

        # building examples and debugging tools
        self.subinfo.options.configure.args += ["-DBUILD_examples=OFF"]
