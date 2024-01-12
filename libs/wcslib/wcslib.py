import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.description = "World Coordinate System Library"
        for ver in ["7.7"]:
            self.targets[ver] = "http://indilib.org/jdownloads/wcslib/wcslib-%s.tar.gz" % ver
            self.targetInstSrc[ver] = "wcslib-%s" % ver
        self.defaultTarget = "7.7"
        if CraftCore.compiler.isMacOS:
            self.patchToApply["7.7"] = [("int64.diff", 1)]
            self.patchLevel["7.7"] = 1

    def setDependencies(self):
        self.runtimeDependencies["libs/cfitsio"] = None


from Package.CMakePackageBase import *


class Package(CMakePackageBase):
    def __init__(self):
        super().__init__()
