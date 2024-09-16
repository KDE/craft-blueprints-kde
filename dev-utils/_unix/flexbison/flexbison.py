import info
from Package.VirtualPackageBase import VirtualPackageBase


class subinfo(info.infoclass):
    def setTargets(self):
        self.targets["latest"] = ""
        self.defaultTarget = "latest"

    def setDependencies(self):
        self.buildDependencies["dev-utils/flex"] = None
        self.buildDependencies["dev-utils/bison"] = None


class Package(VirtualPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.subinfo.shelveAble = False
