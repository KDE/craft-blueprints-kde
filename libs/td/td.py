import info

class subinfo(info.infoclass):
    def setTargets(self):
        self.svnTargets['master'] = 'https://github.com/tdlib/td.git'
        self.targetConfigurePath["master"] = "cmake"
        for ver in ["a68d8e77efb03896f3a04fc316c47136b0bab7df"]:
            self.targets[ver] = f"https://github.com/tdlib/td/archive/{ver}.tar.gz"
            self.archiveNames[ver] = f"td-{ver}.tar.gz"
            self.targetInstSrc[ver] = f"td-{ver}"
            self.targetConfigurePath[ver] = "cmake"

        self.defaultTarget = "a68d8e77efb03896f3a04fc316c47136b0bab7df"

    def setDependencies(self):
        self.buildDependencies["virtual/base"] = None
        self.buildDependencies["libs/zlib"] = None
        self.buildDependencies["libs/openssl"] = None

from Package.CMakePackageBase import *

class Package(CMakePackageBase):
    def __init__(self):
        CMakePackageBase.__init__(self)
