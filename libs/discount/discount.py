import info


class subinfo(info.infoclass):
    def setTargets(self):
        for ver in ["2.2.3a"]:
            self.targets[ver] = f"https://github.com/Orc/discount/archive/v{ver}.zip"
            self.targetInstSrc[ver] = f"discount-{ver}"
            self.archiveNames[ver] = f"discount-{ver}.zip"
            self.targetConfigurePath[ver] = "cmake"

        self.description = "Markdown convering library"
        self.defaultTarget = "2.2.3a"

    def setDependencies(self):
        self.runtimeDependencies["virtual/base"] = "default"

from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self, **args):
        CMakePackageBase.__init__(self)
