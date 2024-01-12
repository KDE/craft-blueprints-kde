import info


class subinfo(info.infoclass):
    def setTargets(self):
        self.targets["latest"] = ""
        self.defaultTarget = "latest"

    def setDependencies(self):
        self.buildDependencies["dev-utils/flex"] = None
        self.buildDependencies["dev-utils/bison"] = None


from Package.VirtualPackageBase import *


class Package(VirtualPackageBase):
    def __init__(self):
        super().__init__()
        self.subinfo.shelveAble = False
