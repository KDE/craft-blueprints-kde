import info

class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets['master'] = 'https://github.com/Samsung/rlottie.git'
        self.targetConfigurePath["master"] = "cmake"
        for ver in ["0.2"]:
            self.targets[ver] = f"https://github.com/Samsung/rlottie/archive/refs/tags/v{ver}.tar.gz"
            self.archiveNames[ver] = f"rlottie-{ver}.tar.gz"
            self.targetInstSrc[ver] = f"rlottie-{ver}"
            self.targetConfigurePath[ver] = "cmake"

        self.defaultTarget = "0.2"

    def setDependencies(self):
        self.buildDependencies["virtual/base"] = None

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
