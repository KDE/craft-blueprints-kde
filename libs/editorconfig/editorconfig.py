import info
from Package.CMakePackageBase import CMakePackageBase
from Utils import CraftHash


class subinfo(info.infoclass):
    def setTargets(self):
        self.description = "EditorConfig core library written in C"

        # use latest stable version
        ver = "0.12.5"
        self.targets[ver] = f"https://github.com/editorconfig/editorconfig-core-c/archive/v{ver}.tar.gz"
        self.targetInstSrc[ver] = f"editorconfig-core-c-{ver}"
        self.targetDigests[ver] = (["b2b212e52e7ea6245e21eaf818ee458ba1c16117811a41e4998f3f2a1df298d2"], CraftHash.HashAlgorithm.SHA256)
        self.defaultTarget = ver

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = None
        self.runtimeDependencies["libs/pcre2"] = None


class Package(CMakePackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
