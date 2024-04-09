import info
from Package.CMakePackageBase import *


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["1.1.2"]:
            self.targets[ver] = f"https://github.com/dlfcn-win32/dlfcn-win32/archive/v{ver}.tar.gz"
            self.targetInstSrc[ver] = f"dlfcn-win32-{ver}"
        self.svnTargets["master"] = "https://github.com/dlfcn-win32/dlfcn-win32.git"
        self.targetDigests["1.1.2"] = (["a4ff75ffa4b8ce90b4be923da69045b2077bba780f792b29f6f46d52d68cbc50"], CraftHash.HashAlgorithm.SHA256)

        self.description = "POSIX dlfcn wrapper for Windows"
        self.webpage = "https://github.com/dlfcn-win32/dlfcn-win32"
        self.defaultTarget = "1.1.2"


class Package(CMakePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
