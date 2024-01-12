import info
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["1.1.37"]:
            self.targets[ver] = f"https://download.gnome.org/sources/libxslt/1.1/libxslt-{ver}.tar.xz"
            self.targetInstSrc[ver] = f"libxslt-{ver}"
        self.patchToApply["1.1.37"] = [("libxslt-1.1.37-20221108.diff", 1)]
        self.targetDigests["1.1.37"] = (["3a4b27dc8027ccd6146725950336f1ec520928f320f144eb5fa7990ae6123ab4"], CraftHash.HashAlgorithm.SHA256)
        self.description = "The GNOME XSLT C library and tools"
        self.webpage = "https://gitlab.gnome.org/GNOME/libxslt"
        self.defaultTarget = "1.1.37"

    def setDependencies(self):
        self.buildDependencies["dev-utils/pkg-config"] = None
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/libxml2"] = None
        self.runtimeDependencies["libs/zlib"] = None
        self.runtimeDependencies["libs/iconv"] = None


class Package(CMakePackageBase):
    def __init__(self, **args):
        super().__init__()
        self.subinfo.options.configure.args += ["-DLIBXSLT_WITH_PYTHON=OFF"]
