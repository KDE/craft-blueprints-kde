import info
from Package.VirtualPackageBase import VirtualPackageBase


class subinfo(info.infoclass):
    def setTargets(self):
        self.targets["latest"] = ""
        self.defaultTarget = "latest"


class Package(VirtualPackageBase):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
