import info
from Package.CMakePackageBase import CMakePackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["2.10.3"]:
            self.svnTargets[ver] = f"https://gitlab.gnome.org/GNOME/libxml2.git||v{ver}"
        self.targetDigests["2.10.3"] = (["497f12e34790d407ec9e2a190d576c0881a1cd78ff3c8991d1f9e40281a5ff57"], CraftHash.HashAlgorithm.SHA256)
        self.description = "XML C parser and toolkit (runtime and applications)"
        self.defaultTarget = "2.10.3"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/zlib"] = None
        self.runtimeDependencies["libs/liblzma"] = None
        self.runtimeDependencies["libs/iconv"] = None
        self.runtimeDependencies["libs/icu"] = None


class Package(CMakePackageBase):
    def __init__(self, **args):
        CMakePackageBase.__init__(self)
        self.subinfo.options.configure.args += ["-DLIBXML2_WITH_PYTHON=OFF"]
